import { NavLink } from "react-router-dom";
import classes from "./MainNavigation.module.css";
import { useQuery } from "@tanstack/react-query";
import appLogicAuth from "../app-logic/app-logic-auth";
import authActions from "../store-localstorage/auth-actions";

const getUserFullName = () => {
  let name = "";
  if (authActions.getAccessToken()) {
    const authDetails = authActions.getAuthDetails();
    name = `${authDetails.firstName} ${authDetails.lastName}`;
  }
  return name;
};

export default function MainNavigation() {
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

  return (
    <header className={`${classes.header}`}>
      <h1 className={`${classes["site-name"]}`}>
        {" "}
        <NavLink to="/">Fai Yip's FastAPI Microservices Demo</NavLink>
      </h1>

      <ul className={`${classes["auth-options"]}`}>
        {!isAuth && (
          <li>
            <NavLink
              className={({ isActive }) =>
                isActive ? classes.active : undefined
              }
              to="/login"
            >
              Login
            </NavLink>
          </li>
        )}
        {!isAuth && (
          <li>
            <NavLink
              className={({ isActive }) =>
                isActive ? classes.active : undefined
              }
              to="/register"
            >
              Register
            </NavLink>
          </li>
        )}
        {isAuth && (
          <li>
            <NavLink
              className={({ isActive }) =>
                isActive ? classes.active : undefined
              }
              to="/logout"
            >
              {getUserFullName()}
            </NavLink>
          </li>
        )}
      </ul>
    </header>
  );
}
