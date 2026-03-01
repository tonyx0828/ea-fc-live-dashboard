"""
WebSocket 连接管理器
处理多个 WebSocket 并发连接
"""
from typing import List
from fastapi import WebSocket
import json
import asyncio


class ConnectionManager:
    """
    WebSocket 连接管理
    
    功能：
    - 管理所有活跃连接
    - 广播消息
    - 心跳检测
    """
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.match_subscriptions: dict = {}  # match_id -> [websockets]
    
    async def connect(self, websocket: WebSocket):
        """接受新连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """断开连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        
        # 清理订阅
        for match_id, connections in self.match_subscriptions.items():
            if websocket in connections:
                connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """发送个人消息"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"❌ 发送消息失败: {e}")
    
    async def broadcast(self, message: dict):
        """广播消息给所有连接"""
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                disconnected.append(connection)
        
        # 清理断开的连接
        for conn in disconnected:
            self.disconnect(conn)
    
    async def broadcast_to_match(self, match_id: int, message: dict):
        """向订阅特定比赛的客户端广播"""
        if match_id not in self.match_subscriptions:
            return
        
        disconnected = []
        for connection in self.match_subscriptions[match_id]:
            try:
                await connection.send_text(json.dumps(message))
            except Exception:
                disconnected.append(connection)
        
        # 清理断开的连接
        for conn in disconnected:
            if conn in self.match_subscriptions[match_id]:
                self.match_subscriptions[match_id].remove(conn)
    
    def subscribe_to_match(self, websocket: WebSocket, match_id: int):
        """订阅特定比赛"""
        if match_id not in self.match_subscriptions:
            self.match_subscriptions[match_id] = []
        self.match_subscriptions[match_id].append(websocket)
    
    def unsubscribe_from_match(self, websocket: WebSocket, match_id: int):
        """取消订阅"""
        if match_id in self.match_subscriptions:
            if websocket in self.match_subscriptions[match_id]:
                self.match_subscriptions[match_id].remove(websocket)
    
    def get_connection_count(self) -> int:
        """获取活跃连接数"""
        return len(self.active_connections)
