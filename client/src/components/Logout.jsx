import { Navigate } from "react-router-dom";
import authActions from "../store-localstorage/auth-actions";
import { useQueryClient } from "@tanstack/react-query";


export default function Logout({redirectUrl}) {
  const queryClient = useQueryClient();
  authActions.clearAuthTokens();
  queryClient.invalidateQueries(["auth"])
  return <Navigate to={redirectUrl} />;
}
