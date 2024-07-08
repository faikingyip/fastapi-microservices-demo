import { useRouteError } from "react-router-dom";

export default function PageError() {
  let status = 0;
  let errors = null;

  const errorsWrapper = useRouteError();

  status = errorsWrapper.status;
  errors = errorsWrapper.errors && errorsWrapper.errors;

  let title = "Sorry, something went wrong!";
  let message = "";

  if (status === 404) {
    message = "The page or resource you're looking for doesn't exist.";
  } else if (status === 500) {
    if (errors.networkError) {
      message =
        "There may be a connection error to the server. Please check your connection and try again.";
    }
  }

  return (
    <div>
      <h1>{title}</h1>
      <p>{message}</p>
    </div>
  );
}
