import { useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { mutateCreateTrans } from "../../tanstackqfns/mutate-create_trans";
import classes from "./FormCreateTrans.module.css";

import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import InputGroup from "../../components/inputs/InputGroup";

const REDIRECT_URL_QUERY_PARAM = "redirectUrl";
const DEFAULT_REDIRECT_URL = "/microservices-demo/";

const schema = z.object({
  amount: z.string().min(1, "Amount is required"),
});

export default function FormCreateTrans({buttonText, buttonTextSubmitting}) {
  const form = useForm({
    mode: "onBlur",
    resolver: zodResolver(schema),
  });

  const { search } = useLocation();
  const queryParams = new URLSearchParams(search);

  const navigate = useNavigate();
  const mutationDeposit = useMutation({
    mutationFn: mutateCreateTrans,
    onSuccess: () => {
      let redirectUrl = queryParams.get(REDIRECT_URL_QUERY_PARAM);
      if (!redirectUrl) {
        redirectUrl = `${DEFAULT_REDIRECT_URL}`;
      }
      navigate(redirectUrl);
    },
    onError: (err) => {
      const serverValErrs = buildServerValErrs(err);
      // if (serverValErrs.invalidCredentials) {
      //   form.setError(ROOT_ERROR_NAME, {
      //     message: INVALID_CREDENTIALS_MSG,
      //   });
      // }
    },
  });

  const serverValErrs = buildServerValErrs(mutationDeposit.error);

  function handleOnSubmit(data) {
    mutationDeposit.mutate({
      payload: data,
    });
  }

  return (
    <form method="post" onSubmit={form.handleSubmit(handleOnSubmit)}>
      <InputGroup
        id="amount"
        label="Amount"
        type="number"
        {...form.register("amount")}
        errorMessage={
          form.formState.errors.amount && form.formState.errors.amount.message
        }
      />

      <div className={`${classes["buttons"]}`}>
        <button
          type="submit"
          disabled={mutationDeposit.isPending}
          className={`button button-color-proceed button-width-stretched`}
        >
          {mutationDeposit.isPending ? buttonTextSubmitting : buttonText}
        </button>
      </div>
    </form>
  );
}

const buildServerValErrs = (err) => {
  let serverValErrs = {
    // uniqueEmail: false,
  };

  if (!err) {
    return serverValErrs;
  }

  if (!err.response) {
    throw err;
  }

  // if (
  //   err.response.data &&
  //   err.response.data.email &&
  //   err.response.data.email.includes("user with this email already exists.")
  // ) {
  //   serverValErrs.uniqueEmail = true;
  // }

  return serverValErrs;
};
