import { useMutation, useQueryClient } from "@tanstack/react-query";
import classes from "./FormEditDetailText.module.css";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import InputGroup from "../../components/inputs/InputGroup";

const REDIRECT_URL_QUERY_PARAM = "redirectUrl";
const DEFAULT_REDIRECT_URL = "/";
const ROOT_ERROR_NAME = "root";
const INVALID_CREDENTIALS_MSG = "The credentials you provided are invalid";

export default function FormEditDetailText({
  fieldName,
  fieldTitle,
  initialFieldValue,
  onCancelClick,
  onSuccess,
  zodSchema,
  mutationFn,
  queriesToInvalidateOnSuccess,
}) {
  const form = useForm({
    mode: "onBlur",
    resolver: zodResolver(zodSchema),
    defaultValues: initialFieldValue
      ? {
          [fieldName]: initialFieldValue,
        }
      : undefined,
  });

  const queryClient = useQueryClient();
  const detailMutator = useMutation({
    mutationFn: mutationFn,
    onSuccess: (res) => {
      queryClient.invalidateQueries(queriesToInvalidateOnSuccess);
      if (onSuccess) {
        onSuccess(res.data);
      }
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

  function handleOnSubmit(data) {
    detailMutator.mutate({
      payload: data,
    });
  }

  return (
    <form method="post" onSubmit={form.handleSubmit(handleOnSubmit)}>
      <InputGroup
        id={fieldName}
        label={fieldTitle}
        type="text"
        {...form.register(fieldName)}
        errorMessage={
          form.formState.errors[fieldName] &&
          form.formState.errors[fieldName].message
        }
      />

      <div className={`${classes["buttons"]}`}>
        <button
          type="button"
          onClick={onCancelClick}
          disabled={detailMutator.isPending}
          className={`button button-color-cancel`}
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={detailMutator.isPending}
          className={`button button-color-proceed`}
        >
          {detailMutator.isPending ? "saving" : "Save"}
        </button>
      </div>

      {/* <RootError
        errorMessage={
          serverValErrs &&
          Object.values(serverValErrs).some((val) => val) &&
          serverValErrs.uniqueTech &&
          "You've already selected this skill. Choose another one."
        }
      /> */}
    </form>
  );
}

const buildServerValErrs = (err) => {
  let serverValErrs = {
    uniqueTech: false,
  };

  if (!err) {
    return serverValErrs;
  }

  if (!err.response) {
    throw err;
  }

  // if (err.response.data && err.response.data.unique_tech) {
  //   serverValErrs.uniqueTech = true;
  // }

  return serverValErrs;
};
