# WebSocket Events

Base Path: `ws://<host>/api/v1/stream/ws/{topic}`

## Connection
The application exposes a real-time stream via the WebSockets manager (`ws_manager`). 

### Supported Topics
The `{topic}` path parameter can be used to subscribe to different streams:
- `live_events`: Stream of live event occurrences and map updates.
- `gori_alerts`: High GORI (Grid Operations Risk Index) alerts.
- `deployment_alerts`: AI-driven resource deployment actions.

## Lifecycle
1. **Connect**: Clients open connection to the topic.
2. **Keep Alive**: Clients can send heartbeats or text to keep the connection alive.
3. **Disconnect**: Clean disconnection handled by `ws_manager`.
