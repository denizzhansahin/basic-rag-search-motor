import { io, Socket } from "socket.io-client";

export const socket: Socket = io(
  import.meta.env.VITE_HOST_URL || window.location.origin,
  {
    autoConnect: true,
    transports: ["websocket"],
  }
);