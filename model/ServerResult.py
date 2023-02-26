import copy
import engine.LogManager as LogManager
import logic.XmlParse as XmlParse

HttpCodeString = {
    -1: "断网",
    404: "404 未找到网页",
    500: "500 服务器错误",
}


class ServerResult:
    """返回结果"""
    def __init__(self, url: str, result: str):
        self.logger = LogManager.GetLogger(self.__class__.__name__)
        self.url = url
        self.http_code = 0
        self.success = False
        self.xml = ""
        self.error = ""
        self.result: dict = None
        self.result_map: dict = {}
        self._HandleXmlString(result)

    def _HandleXmlString(self, result: str) -> None:
        if not result:
            return

        if result.startswith("code:"):
            self.http_code = int(result.replace("code:", ""))
            return

        self.http_code = 200
        if result.startswith("E"):
            self.error = result
            return

        try:
            # 过滤掉非法字符&
            result = result.replace("&", "")
            self.result: dict = XmlParse.Parse(result)["results"]
            if self.result.get("state", "0") == "1":
                self.success = True
                self.xml = result
                return

            if "message" in self.result:
                self.error = self.result["message"]
            elif "exception" in self.result:
                self.error = self.result["exception"]

            if not self.error:
                self.error = result
        except Exception:
            self.error = result
            self.logger.LogLastExcept()

    def IsHttpSucceed(self) -> False:
        return self.http_code == 200

    def GetHttpErrorInfo(self) -> str:
        return HttpCodeString.get(self.http_code, f"错误码：{self.http_code}")

    def GetDebugInfo(self) -> str:
        if not self.IsHttpSucceed():
            return self.GetHttpErrorInfo()
        elif not self.success:
            return self.error
        return self.xml

    def GetUrl(self) -> str:
        return self.url

    def GetValue(self, key: str, default=None):
        if not self.result_map:
            self.result_map = self._HandleKeyValue(copy.deepcopy(self.result))

        value = self.result_map
        try:
            for k in key.split("."):
                value = value[k]
        except Exception:
            value = default
        return value

    def GetValueList(self, key: str):
        value = self.GetValue(key, [])
        if not isinstance(value, list):
            value = [value]
        return value

    def _HandleKeyValue(self, value):
        if isinstance(value, dict):
            for k, v in value.items():
                value[k] = self._HandleKeyValue(v)
            return value

        if isinstance(value, list):
            for k, v in enumerate(value):
                value[k] = self._HandleKeyValue(v)
            return value

        try:
            return eval(value)
        except Exception:
            return value
