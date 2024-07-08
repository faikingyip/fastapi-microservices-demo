import { useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { mutateCreateVacancy } from "../../tanstackqfns/mutate-create-vacancy";
import classes from "./FormCreateVacancy.module.css";

import {
  isWithinMaxValue,
  isWithinMinValue,
} from "../../utils/utils-number_validation";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import InputGroup from "../../components/inputs/InputGroup";
import CheckboxGroup from "../../components/inputs/CheckoxGroup";

const REDIRECT_URL_QUERY_PARAM = "redirectUrl";
const DEFAULT_REDIRECT_URL = "/employer/vacancies/";
// const ROOT_ERROR_NAME = "root";
const DIGITS_ONLY = /^\d+$/;

const schema = z
  .object({
    title: z.string().min(1, "Job title is required"),
    candidates_needed: z
      .string()
      .min(1, "Enter number of candidates needed")
      .regex(DIGITS_ONLY, "Digits only")
      .refine((val) => isWithinMinValue(val, 1), {
        message: "At least 1 candidate needed",
      })
      .refine((val) => isWithinMaxValue(val, 1000), {
        message: "Max of 1000 candidates allowed",
      }),
    days_in_office: z
      .string()
      .min(1, "Enter days required in the office")
      .regex(DIGITS_ONLY, "Digits only")
      .refine((val) => isWithinMinValue(val, 0), {
        message: "Enter between 1 and 7 days, or 0 for fully remote",
      })
      .refine((val) => isWithinMaxValue(val, 7), {
        message: "Enter between 1 and 7 days, or 0 for fully remote",
      }),
    work_address: z.string().optional(),
    work_city: z.string().optional(),
    is_hiring: z.string().optional(),
  })
  .refine(
    (data) => {
      if (!data.work_city && data.days_in_office && data.days_in_office > 0) {
        return false;
      }
      return true;
    },
    {
      message: "Work office is required if job requires some days in office",
      path: ["work_city"],
    }
  );

export default function FormCreateVacancy() {
  const form = useForm({
    mode: "onBlur",
    resolver: zodResolver(schema),
  });

  const { search } = useLocation();
  const queryParams = new URLSearchParams(search);

  const navigate = useNavigate();
  const mutationCreateVacancy = useMutation({
    mutationFn: mutateCreateVacancy,
    onSuccess: (res) => {
      let redirectUrl = queryParams.get(REDIRECT_URL_QUERY_PARAM);
      if (!redirectUrl) {
        redirectUrl = `${DEFAULT_REDIRECT_URL}${res.data.id}`;
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

  const serverValErrs = buildServerValErrs(mutationCreateVacancy.error);

  const handleBlur = async (fieldName) => {
    if (fieldName === "days_in_office") {
      if (form.formState.errors.work_city) {
        await form.trigger("work_city");
      }
    }
  };

  const handleDigitOnlyChange = (event, fieldName) => {
    const { value } = event.target;
    const digitOnlyValue = value.replace(/\D/g, "");
    form.setValue(fieldName, digitOnlyValue, {
      shouldValidate: false,
      shouldDirty: false,
    });
  };

  function handleOnSubmit(data) {
    mutationCreateVacancy.mutate({
      payload: data,
    });
  }

  return (
    <form method="post" onSubmit={form.handleSubmit(handleOnSubmit)}>
      <InputGroup
        id="jobTitle"
        label="Job title"
        type="text"
        {...form.register("title")}
        errorMessage={
          form.formState.errors.title && form.formState.errors.title.message
        }
        maxLength="254"
      />

      <InputGroup
        id="candidatesNeeded"
        label="Candidates needed"
        type="text"
        // {...form.register("candidates_needed")}
        {...form.register("candidates_needed", {
          onChange: (event) =>
            handleDigitOnlyChange(event, "candidates_needed"),
        })}
        errorMessage={
          form.formState.errors.candidates_needed &&
          form.formState.errors.candidates_needed.message
        }
        maxLength="4"
      />

      <InputGroup
        id="daysInOffice"
        label="Days in office"
        type="text"
        {...form.register("days_in_office", {
          onChange: (event) => handleDigitOnlyChange(event, "days_in_office"),
          onBlur: () => handleBlur("days_in_office"),
        })}
        errorMessage={
          form.formState.errors.days_in_office &&
          form.formState.errors.days_in_office.message
        }
        maxLength="1"
      />

      <InputGroup
        id="workAddress"
        label="Work address"
        type="text"
        {...form.register("work_address")}
        errorMessage={
          form.formState.errors.work_address &&
          form.formState.errors.work_address.message
        }
        maxLength="1000"
      />

      <InputGroup
        id="workCity"
        label="Work city"
        type="text"
        {...form.register("work_city")}
        errorMessage={
          form.formState.errors.work_city &&
          form.formState.errors.work_city.message
        }
        maxLength="100"
      />

      <CheckboxGroup
        id="isHiring"
        label="Is the position open now?"
        name="is_hiring"
        // type="checkbox"
        {...form.register("is_hiring")}
      />

      <div className={`${classes["buttons"]}`}>
        <button
          type="submit"
          disabled={mutationCreateVacancy.isPending}
          className={`button button-color-proceed button-width-stretched`}
        >
          {mutationCreateVacancy.isPending ? "Submitting" : "Submit"}
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
