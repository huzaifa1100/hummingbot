import asyncio
import logging
from typing import List, Optional

from hummingbot.connector.exchange.wazirx.wazirx_api_user_stream_data_source import WazirxAPIUserStreamDataSource
from hummingbot.connector.exchange.wazirx.wazirx_auth import WazirxAuth
from hummingbot.connector.exchange.wazirx.wazirx_constants import EXCHANGE_NAME
from hummingbot.core.data_type.user_stream_tracker import UserStreamTracker
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.logger import HummingbotLogger


class WazirxUserStreamTracker(UserStreamTracker):
    _cbpust_logger: Optional[HummingbotLogger] = None

    @classmethod
    def logger(cls) -> HummingbotLogger:
        if cls._bust_logger is None:
            cls._bust_logger = logging.getLogger(__name__)
        return cls._bust_logger

    def __init__(
            self,
            wazirx_auth: Optional[WazirxAuth] = None,
            trading_pairs: Optional[List[str]] = None,
    ):
        self._wazirx_auth: WazirxAuth = wazirx_auth
        super().__init__(data_source=WazirxAPIUserStreamDataSource(
            wazirx_auth=self._wazirx_auth
        ))
        self._trading_pairs: List[str] = trading_pairs or []

    @property
    def data_source(self) -> UserStreamTrackerDataSource:
        if not self._data_source:
            self._data_source = WazirxAPIUserStreamDataSource(
                wazirx_auth=self._wazirx_auth
            )
        return self._data_source

    @property
    def exchange_name(self) -> str:
        return EXCHANGE_NAME

    async def start(self):
        self._user_stream_tracking_task = asyncio.ensure_future(
            self.data_source.listen_for_user_stream(self._user_stream)
        )
        await asyncio.gather(self._user_stream_tracking_task)
