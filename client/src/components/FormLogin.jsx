import React from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import classes from "./FormLogin.module.css";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import authActions from "../store-localstorage/auth-actions";
import {
  extractAccessToken,
  extractRefreshToken,
} from "../store-backend/utils/extract-res";
import { useLocation, useNavigate } from "react-router-dom";
import { mutateLogin } from "../tanstackqfns/mutate-login";
import InputGroup from "./inputs/InputGroup";
import RootError from "./inputs/RootError";

const REDIRECT_URL_QUERY_PARAM = "redirectUrl";
const DEFAULT_REDIRECT_URL = "/";
const ROOT_ERROR_NAME = "root"
const INVALID_CREDENTIALS_MSG = "The credentials you provided are invalid"

const schema = z.object({
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Invalid email address" }),
  password: z.string().min(1, { message: "Password is required" }),
});

export default function FormLogin() {
  const form = useForm({
    mode: "onBlur",
    resolver: zodResolver(schema),
  });

  const { search } = useLocation();
  const queryParams = new URLSearchParams(search);
  let redirectUrl = queryParams.get(REDIRECT_URL_QUERY_PARAM);
  if (!redirectUrl) {
    redirectUrl = DEFAULT_REDIRECT_URL;
  }
  const queryClient = useQueryClient();

  const navigate = useNavigate();
  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: mutateLogin,
    onSuccess: (res) => {
      authActions.storeAuthTokens({
        accessToken: extractAccessToken(res),
        refreshToken: extractRefreshToken(res),
      });
      queryClient.invalidateQueries({
        queryKey: ["auth"],
      });
      navigate(redirectUrl);
    },
    onError: (err) => {
      const serverValErrs = buildServerValErrs(err);
      if (serverValErrs.invalidCredentials) {
        form.setError(ROOT_ERROR_NAME, {
          message: INVALID_CREDENTIALS_MSG,
        });
      }
    },
  });

  function handleOnSubmit(data) {
    mutate({
      payload: data,
    });
  }

  return (
    <form method="post" onSubmit={form.handleSubmit(handleOnSubmit)}>
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
          {isPending ? "Logging in" : "Login"}
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
    invalidCredentials: false,
  };

  if (!err) {
    return serverValErrs;
  }

  if (!err.response) {
    throw err;
  }

  if (err.response.status == 401) {
    serverValErrs.invalidCredentials = true;
  }

  return serverValErrs;
};
