import {
  isWithinMaxValue,
  isWithinMinValue,
} from "../../utils/utils-number_validation";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { mutateCreateTechKnowledge } from "../../tanstackqfns/mutate-create-tech-knowledge";
import classes from "./FormAddSkillExp.module.css";
import RootError from "../../components/inputs/RootError";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import InputGroup from "../../components/inputs/InputGroup";
import SelectGroup from "../../components/inputs/SelectGroup";

const ROOT_ERROR_NAME = "root";
const DIGITS_ONLY = /^\d+$/;
const TECH_ALREADY_SELECTED_MSG =
  "You've already selected this tech. Choose another one.";

const schema = z.object({
  tech: z.string().min(1, "Choose a tech"),
  year_of_first_exposure: z
    .string()
    .min(1, "Enter a year of first exposure")
    .regex(DIGITS_ONLY, "Digits only")
    .refine((val) => isWithinMinValue(val, 1950), {
      message: "Enter a year from 1950",
    })
    .refine((val) => isWithinMaxValue(val, new Date().getFullYear()), {
      message: "Enter a year not in the future",
    }),
  months_of_practice: z
    .string()
    .min(1, "Enter number of active months of practice")
    .regex(DIGITS_ONLY, "Digits only")
    .refine((val) => isWithinMinValue(val, 1), {
      message: "Enter a number no less than 1",
    })
    .refine((val) => isWithinMaxValue(val, 120), {
      message: "Enter a number no greater than 120",
    }),
});

export default function FormAddSkillExp({
  chooseSkillLabel,
  yearOfExposureLabel,
  monthsOfPracticeLabel,
  onCancelClick,
  onSuccess,
  skills,
}) {
  const form = useForm({
    mode: "onBlur",
    resolver: zodResolver(schema),
  });

  const queryKey = ["tech-knowledge"];

  const queryClient = useQueryClient();
  const { mutate, isPending, isError, error } = useMutation({
    mutationFn: mutateCreateTechKnowledge,
    onSuccess: (res) => {
      queryClient.invalidateQueries(queryKey);
      if (onSuccess) {
        onSuccess(res.data);
      }
    },
    onError: (err) => {
      const serverValErrs = buildServerValErrs(err);
      if (serverValErrs.uniqueTech) {
        form.setError(ROOT_ERROR_NAME, {
          message: TECH_ALREADY_SELECTED_MSG,
        });
      }
    },
  });

  // DUPLICATED
  const handleDigitOnlyChange = (event, fieldName) => {
    const { value } = event.target;
    const digitOnlyValue = value.replace(/\D/g, "");
    form.setValue(fieldName, digitOnlyValue, {
      shouldValidate: false,
      shouldDirty: false,
    });
  };

  function handleOnSubmit(data) {
    mutate({
      payload: data,
    });
  }

  return (
    <form method="post" onSubmit={form.handleSubmit(handleOnSubmit)}>
      <SelectGroup
        id="tech"
        label={chooseSkillLabel}
        options={skills.results}
        valueFieldName="id"
        textFieldName="name"
        {...form.register("tech")}
      />

      <InputGroup
        id="yearOfFirstExp"
        label={yearOfExposureLabel}
        type="text"
        {...form.register("year_of_first_exposure", {
          onChange: (event) =>
            handleDigitOnlyChange(event, "year_of_first_exposure"),
        })}
        errorMessage={
          form.formState.errors.year_of_first_exposure &&
          form.formState.errors.year_of_first_exposure.message
        }
        maxLength="4"
      />

      <InputGroup
        id="monthsOfPractice"
        label={monthsOfPracticeLabel}
        type="text"
        {...form.register("months_of_practice", {
          onChange: (event) =>
            handleDigitOnlyChange(event, "months_of_practice"),
        })}
        errorMessage={
          form.formState.errors.months_of_practice &&
          form.formState.errors.months_of_practice.message
        }
        maxLength="3"
      />

      <div className={`${classes["buttons"]}`}>
        <button
          type="button"
          onClick={onCancelClick}
          disabled={isPending}
          className={`button button-color-cancel`}
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isPending}
          className={`button button-color-proceed`}
        >
          {isPending ? "submitting" : "Submit"}
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
    uniqueTech: false,
  };

  if (!err) {
    return serverValErrs;
  }

  if (!err.response) {
    throw err;
  }

  if (err.response.data && err.response.data.unique_tech) {
    serverValErrs.uniqueTech = true;
  }

  return serverValErrs;
};
