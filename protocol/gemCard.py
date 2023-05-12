import manager.ProtocolMgr as ProtocolMgr
from model.child import *  # noqa: F403

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.Account import Account
    from model.ServerResult import ServerResult


@ProtocolMgr.Protocol("宝石翻牌")
async def getGemCardInfo(account: 'Account', result: 'ServerResult'):
    if result.success:
        info = {
            "免费翻倍次数": result.GetValue("gemcardinfo.freedouble"),
            "翻倍花费金币": result.GetValue("doublecost"),
            "免费升级次数": result.GetValue("freeupgradetimes"),
            "升级花费金币": result.GetValue("gemcardinfo.upgradegold"),
            "升级次数": result.GetValue("gemcardinfo.upgradetimes"),
            "组合倍数": result.GetValue("gemcardinfo.comboxs"),
            "免费次数": result.GetValue("gemcardinfo.freetimes"),
            "购买次数花费金币": result.GetValue("gemcardinfo.buygold"),
            "卡牌": [{"id": idx, "combo": combo} for idx, combo in enumerate(result.GetValue("gemcardinfo.gemcardliststring"))],
        }
        return info


@ProtocolMgr.Protocol("领取", ("cost", "doubleCard", "list"))
async def receiveGem(account: 'Account', result: 'ServerResult', cost, doubleCard, list, double_cost, cost_cost, baoshi):
    if result.success:
        reward_info = RewardInfo()  # noqa: F405
        reward = Reward()  # noqa: F405
        reward.type = 5
        reward.lv = 1
        reward.num = baoshi
        reward_info.reward.append(reward)
        account.logger.info("花费%d金币翻倍, 花费%d金币升级, 领取翻牌奖励, 获得%s", double_cost, cost_cost, reward_info)
