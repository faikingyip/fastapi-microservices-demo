import { NavLink } from "react-router-dom";
import classes from "./MainNavigation.module.css";
import { useQuery } from "@tanstack/react-query";
import appLogicAuth from "../app-logic/app-logic-auth";
import authActions from "../store-localstorage/auth-actions";

const getJobseekerName = () => {
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
        <NavLink to="/">Codelocks Recruitment</NavLink>
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
              {getJobseekerName()}
            </NavLink>
          </li>
        )}
      </ul>

      {/* <nav className={`${classes.navbar}`}>
        <div className={`${classes["logo-area"]}`}></div>
        <ul className={`${classes["menu-items"]}`}>
          <li>
            <span
              className={`${classes["menu-item-header"]} ${classes["no-underline"]}`}
            >
              &nbsp;
            </span>
            <ul>

              <li>
                <NavLink to="#">About us</NavLink>
              </li>
              <li>
                <NavLink to="#">Contact</NavLink>
              </li>
            </ul>
          </li> */}
      {/* <li>
            <NavLink to="/counter">Counter</NavLink>
          </li> */}
      {/* <li>
            <span className={`${classes["menu-item-header"]}`}>Employers</span>
            <ul>
              <li>
                <NavLink to="/">Tell us about a vacancy</NavLink>
              </li>
              <li>
                <NavLink to="/">Search jobseekers</NavLink>
              </li>
            </ul>
          </li>
          <li>
            <span className={`${classes["menu-item-header"]}`}>Jobseekers</span>
            <ul>
              <li>
                <NavLink
                  className={({ isActive }) =>
                    isActive ? classes.active : undefined
                  }
                  to="/build-my-job-search-profile"
                >
                  Publish your job interests
                </NavLink>
              </li>
              <li>
                <NavLink
                  className={({ isActive }) =>
                    isActive ? classes.active : undefined
                  }
                  to="/search-jobs"
                >
                  Search jobs
                </NavLink>
              </li>
              <li>
                <NavLink
                  className={({ isActive }) =>
                    isActive ? classes.active : undefined
                  }
                  to="/set-job-alerts"
                >
                  Set up your job alerts
                </NavLink>
              </li>
            </ul>
          </li>
        </ul>
      </nav> */}
    </header>
  );
}
