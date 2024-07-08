import { Navigate, useLocation, useParams } from "react-router-dom";

import { useQuery } from "@tanstack/react-query";
import appLogicAuth from "../../app-logic/app-logic-auth";

export default function ProtectedRoute({
  redirectUrl,
  redirectUrlFn,
  children,
}) {
  /**
   * Wrap the target component with this component to protect it.
   */
  const {
    data: isAuth,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["auth"],
    queryFn: appLogicAuth.isAuthenticated,
    staleTime: 10,
    gcTime: 0,
  });

  const params = useParams();
  const location = useLocation();

  if (redirectUrl && redirectUrlFn) {
    throw new Error(
      "You can only specify either redirectUrl or redirectUrlFn, but not both."
    );
  }

  if (isLoading) {
    return null;
  }

  if (!isAuth) {
    if (redirectUrl) {
      return <Navigate to={redirectUrl} replace />;
    }

    if (redirectUrlFn) {
      return <Navigate to={redirectUrlFn(location, params)} replace />;
    }
  }

  return children;

  // const isAuthenticated = useRouteLoaderData(ROOT);
  // return isAuthenticated ? children : <Navigate to={redirectUrl} />;
}
