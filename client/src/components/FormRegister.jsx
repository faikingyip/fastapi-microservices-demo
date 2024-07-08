import { useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { mutateCreateMe } from "../tanstackqfns/mutate-create-me";
import classes from "./FormRegister.module.css";
import RootError from "./inputs/RootError";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import InputGroup from "./inputs/InputGroup";

const REDIRECT_URL_QUERY_PARAM = "redirectUrl";
const PASSWORD_MAX_LENGTH = 128;
const ROOT_ERROR_NAME = "root";
const REDIRECT_URL = "/login";
const ALREADY_REGISTERED_EMAIL_MSG =
  "The email address you provided is already registered with us.";

const schema = z.object({
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Invalid email address" }),
  password: z
    .string()
    .min(1, { message: "Password is required" })
    .max(PASSWORD_MAX_LENGTH, { message: `Max length ${PASSWORD_MAX_LENGTH}` }),
  first_name: z.string().min(1, { message: "First name is required" }),
  last_name: z.string().min(1, { message: "Last name is required" }),
});

export default function FormRegister() {
  const form = useForm({
    mode: "onBlur",
    resolver: zodResolver(schema),
  });

  const { search } = useLocation();
  const queryParams = new URLSearchParams(search);
  let redirectUrl = queryParams.get(REDIRECT_URL_QUERY_PARAM);
  if (!redirectUrl) {
    redirectUrl = REDIRECT_URL;
  }
  const navigate = useNavigate();
  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: mutateCreateMe,
    onSuccess: (res) => {
      navigate(redirectUrl);
    },
    onError: (err) => {
      const serverValErrs = buildServerValErrs(err);
      if (serverValErrs.uniqueEmail) {
        form.setError(ROOT_ERROR_NAME, {
          message: ALREADY_REGISTERED_EMAIL_MSG,
        });
      }
    },
  });

  const serverValErrs = buildServerValErrs(error);

  function handleOnSubmit(data) {
    mutate({
      payload: data,
    });
  }

  return (
    <form method="post" onSubmit={form.handleSubmit(handleOnSubmit)}>
      <InputGroup
        id="firstName"
        label="First name"
        type="text"
        {...form.register("first_name")}
        errorMessage={
          form.formState.errors.first_name &&
          form.formState.errors.first_name.message
        }
      />

      <InputGroup
        id="lastName"
        label="Last name"
        type="text"
        {...form.register("last_name")}
        errorMessage={
          form.formState.errors.last_name &&
          form.formState.errors.last_name.message
        }
      />

      <InputGroup
        id="email"
        label="Email"
        type="text"
        {...form.register("email")}
        errorMessage={
          form.formState.errors.email && form.formState.errors.email.message
        }
      />

      <InputGroup
        id="password"
        label="Password"
        type="password"
        {...form.register("password")}
        errorMessage={
          form.formState.errors.password &&
          form.formState.errors.password.message
        }
      />

      <div className={`${classes["buttons"]}`}>
        <button
          type="submit"
          disabled={isPending}
          className={`button button-color-proceed button-width-stretched`}
        >
          {isPending ? "Registering" : "Register"}
        </button>
      </div>

      <RootError
        errorMessage={
          form.formState.errors.root && form.formState.errors.root.message
        }
      />
    </form>
  );
}

const buildServerValErrs = (err) => {
  let serverValErrs = {
    uniqueEmail: false,
  };

  if (!err) {
    return serverValErrs;
  }

  if (!err.response) {
    throw err;
  }

  if (
    err.response.data &&
    err.response.data.email &&
    err.response.data.email.includes("user with this email already exists.")
  ) {
    serverValErrs.uniqueEmail = true;
  }

  return serverValErrs;
};
