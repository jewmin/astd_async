# flake8: noqa
from logic.Config import config
from task.BaseTask import BaseTask
from protocol import *


class CityTask(BaseTask):
    def __init__(self, account):
        super().__init__(account)
        self.name = "建造"

    async def _Exec(self):
        await mainCity.mainCity(self.account)

        low_city_dto_list = []
        high_city_dto_list = []
        for main_city_dto in self.account.user.maincitydto:
            if main_city_dto.buildlevel == self.account.user.playerlevel:
                continue
            if main_city_dto.buildname in config["mainCity"]["build_list"]:
                if main_city_dto.cdtime < 240:
                    low_city_dto_list.append(main_city_dto)
                else:
                    high_city_dto_list.append(main_city_dto)

        if not low_city_dto_list and not high_city_dto_list:
            return self.next_half_hour

        low_city_dto_list.sort(key=lambda dto: config["mainCity"]["build_list"].index(dto.buildname))
        high_city_dto_list.sort(key=lambda dto: config["mainCity"]["build_list"].index(dto.buildname))
        cd_time = -1
        constructor = None
        for constructor_dto in self.account.user.constructordto:
            if not (constructor_dto.cdflag == 1 and constructor_dto.ctime > 0):
                constructor = constructor_dto
                break
            elif cd_time < 0 or cd_time > constructor_dto.ctime:
                cd_time = constructor_dto.ctime

        if constructor is None:
            return cd_time

        if constructor.ctime > 0:
            city_dto_list_list = (high_city_dto_list, low_city_dto_list)
        else:
            city_dto_list_list = (low_city_dto_list, high_city_dto_list)

        for city_dto_list in city_dto_list_list:
            if city_dto_list:
                await mainCity.upgradeLevel(self.account, player_BuildingId=city_dto_list[0].id, main_city_dto=city_dto_list[0])
                return self.immediate
