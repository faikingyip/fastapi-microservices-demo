import "./reset.css";
import "./base.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import PageHome from "./pages/PageHome";
import PageLogin from "./pages/PageLogin";
import PageRegister from "./pages/PageRegister";
import PageSearchJobs from "./pages/PageSearchJobs";
import PageSetJobAlerts from "./pages/PageSetJobAlerts";
import LayoutRoot from "./pages/LayoutRoot";
import PageError from "./pages/PageError";
import Logout from "./components/Logout";
import PageCounter from "./pages/PageCounter";

import PageJobseekerSkillset from "./jobseeker/pages/PageJobseekerSkillset";

import ProtectedRoute from "./components/routing/ProtectedRoute";
import PageEmployerRep from "./employer/pages/PageEmployerRep";
import PageSubmitVacancy from "./employer/pages/PageSubmitVacancy";
import PageEmployerVacancies from "./employer/pages/PageEmployerVacancies";
import PageVacancyDetail from "./employer/pages/PageVacancyDetail";

function getRedirectUrlFromQueryParam({ request }, defaultRedirectUrl = null) {
  return (
    new URL(request.url).searchParams.get("redirectUrl") || defaultRedirectUrl
  );
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <LayoutRoot />,
    // errorElement: <PageError />,
    children: [
      {
        index: true,
        element: <PageHome />,
      },
      {
        path: "counter",
        element: (
          <ProtectedRoute redirectUrl="/login">
            <PageCounter />
          </ProtectedRoute>
        ),
      },
      {
        path: "login",
        element: <PageLogin />,
      },
      { path: "logout", element: <Logout redirectUrl="/" /> },
      {
        path: "register",
        element: <PageRegister />,
      },
      {
        path: "build-my-job-search-profile",
        element: (
          <ProtectedRoute redirectUrl="/login?redirectUrl=/build-my-job-search-profile">
            <PageJobseekerSkillset />
          </ProtectedRoute>
        ),
      },
      { path: "search-jobs", element: <PageSearchJobs /> },
      {
        path: "set-job-alerts",
        element: (
          <ProtectedRoute redirectUrl="/login?redirectUrl=/search-jobs">
            <PageSetJobAlerts />
          </ProtectedRoute>
        ),
      },
      {
        path: "submit-vacancy",
        element: (
          <ProtectedRoute redirectUrl="/login?redirectUrl=/submit-vacancy">
            <PageSubmitVacancy />
          </ProtectedRoute>
        ),
      },
      {
        path: "employer/vacancies/:id",
        element: (
          <ProtectedRoute
            redirectUrlFn={(location, params) =>
              `/login?redirectUrl=${encodeURIComponent(
                `/employer/vacancies/${params.id}`
              )}`
            }
          >
            <PageVacancyDetail />
          </ProtectedRoute>
        ),
      },
      {
        path: "build-employer-profile",
        element: (
          <ProtectedRoute redirectUrl="/login?redirectUrl=/build-employer-profile">
            <PageEmployerRep />
          </ProtectedRoute>
        ),
      },
      {
        path: "employer/vacancies",
        element: (
          <ProtectedRoute redirectUrl="/login?redirectUrl=/employer/vacancies">
            <PageEmployerVacancies />
          </ProtectedRoute>
        ),
      },
    ],
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
