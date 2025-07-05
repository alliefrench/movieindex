import { StackClientApp } from "@stackframe/react";
import { useNavigate } from "react-router-dom";

export const stackClientApp = new StackClientApp({
  // You should store these in environment variables
  projectId: "...",
  publishableClientKey: "...",
  tokenStore: "cookie",
  redirectMethod: {
    useNavigate,
  },
});
