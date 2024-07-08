import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";
import { queryVacancy } from "../../tanstackqfns/query-vacancy";
import DetailDisplayText from "../detail/DetailDisplayText";
import { mutatePatchVacancy } from "../../tanstackqfns/mutate-patch-vacancy";
import { z } from "zod";
import {
  isWithinMaxValue,
  isWithinMinValue,
} from "../../utils/utils-number_validation";
import { formatDate } from "../../utils/utils-formatter";
import LiSkillRequirement from "../list-item/LiSkillRequirement";
import classes from "./PageVacancyDetail.module.css";
import { useState } from "react";
import Modal from "../../components/Modal";

const DIGITS_ONLY = /^\d+$/;

const vacancySchema = z.object({
  // work_city: z.string().optional(),
});
// .refine(
//   (data) => {
//     if (!data.work_city && data.days_in_office && data.days_in_office > 0) {
//       return false;
//     }
//     return true;
//   },
//   {
//     message: "Work office is required if job requires some days in office",
//     path: ["work_city"],
//   }
// );

export default function PageVacancyDetail() {
  const params = useParams();

  const queryKey = ["employer-vacancies", params.id];

  const queryEmployerVacancy = useQuery({
    queryKey: queryKey,
    queryFn: () => queryVacancy({ id: params.id }),
    staleTime: 1000 * 60 * 5,
  });

  const mutatePatchVacancyFn = async ({ payload }) => {
    return await mutatePatchVacancy({ id: params.id, payload: payload });
  };

  const [showBindTechnologyForm, setShowBindTechnologyForm] = useState(false);

  function handleShowBindTechnologyFormOnClick() {
    setShowBindTechnologyForm(true);
  }

  function handleBindTechnologyOnCancelClick() {
    setShowBindTechnologyForm(false);
  }

  function handleOnTechKnowedgeCreationSuccess() {
    setShowBindTechnologyForm(false);
  }

  let content;
  if (queryEmployerVacancy.isPending) {
    content = <div>Loading...</div>;
  }

  if (queryEmployerVacancy.isError) {
    throw queryEmployerVacancy.error;
  }

  if (queryEmployerVacancy.data) {
    const vac = queryEmployerVacancy.data.data;
    content = (
      <ul>
        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="title"
            fieldTitle="Title"
            fieldValue={vac.title}
            zodSchema={z.object({
              title: z.string().min(1, "Job title is required"),
            })}
            mutationFn={mutatePatchVacancyFn}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>
        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="days_in_office"
            fieldTitle="Days in office"
            fieldValue={vac.days_in_office}
            zodSchema={z.object({
              days_in_office: z
                .string()
                .regex(DIGITS_ONLY, "Digits only")
                .refine((val) => isWithinMinValue(val, 0), {
                  message: "Enter between 1 and 7 days, or 0 for fully remote",
                })
                .refine((val) => isWithinMaxValue(val, 7), {
                  message: "Enter between 1 and 7 days, or 0 for fully remote",
                }),
            })}
            mutationFn={mutatePatchVacancyFn}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>
        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="work_address"
            fieldTitle="Work address"
            fieldValue={vac.work_address}
            zodSchema={z.object({
              work_address: z.string().optional(),
            })}
            mutationFn={mutatePatchVacancyFn}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>
        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="work_city"
            fieldTitle="Work city"
            fieldValue={vac.work_city}
            zodSchema={z.object({
              work_city: z.string().optional(),
            })}
            mutationFn={mutatePatchVacancyFn}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>

        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="candidates_needed"
            fieldTitle="Candidates needed"
            fieldValue={vac.candidates_needed}
            zodSchema={z.object({
              candidates_needed: z
                .string()
                .regex(DIGITS_ONLY, "Digits only")
                .refine((val) => isWithinMinValue(val, 1), {
                  message: "At least 1 candidate needed",
                })
                .refine((val) => (val, 1000), {
                  message: "Max of 1000 cisWithinMaxValueeandidates allowed",
                }),
            })}
            mutationFn={mutatePatchVacancyFn}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>

        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="is_hiring"
            fieldTitle="Is hiring"
            fieldValue={vac.is_hiring}
            zodSchema={z.object({
              is_hiring: z.string().optional(),
            })}
            mutationFn={mutatePatchVacancyFn}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>

        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="created_on"
            fieldTitle="Created on"
            fieldValue={formatDate(new Date(vac.created_on))}
          />
        </li>
      </ul>
    );
  }

  return (
    <>
      <hr />
      <section className={`section`}>
        {queryEmployerVacancy.data && (
          <h2 className={`section-title section-title-color-wood`}>
            {queryEmployerVacancy.data.data.title}
          </h2>
        )}

        <p className={`section-pitch-text`}>
          Vacancy details
        </p>

        <div className={`section-body`}>{content}</div>
      </section>
      <section
        className={`section section-divider section-back-color-light-purple`}
      >
        <h2 className={`section-title section-title-color-wood`}>
          Tech skill requirements
        </h2>

        <p className={`section-pitch-text`}>
          Tell us about the skills you require for this position.
        </p>

        <div className={`section-body`}>
          <ul>
            <li className={`list-item`}>
              <LiSkillRequirement skillName={"Django"} requirementLevel={1} />
              <hr />
            </li>

            <li className={`list-item`}>
              <LiSkillRequirement
                skillName={"React Tanstack Query Library"}
                requirementLevel={1}
              />
            </li>
          </ul>
        </div>
      </section>
      <section className={`section ${classes["add-tech"]}`}>
        <button
          type="button"
          disabled={showBindTechnologyForm}
          onClick={handleShowBindTechnologyFormOnClick}
          className={`button button-width-stretched button-color-proceed`}
        >
          Add tech
        </button>

        {showBindTechnologyForm && (
          <Modal onClose={handleBindTechnologyOnCancelClick}>
            <div className={`form-container`}>
              <h2 className={`form-title`}>Add a tech requirement</h2>
              {/* <FormAddSkillExp
                skills={techs.data}
                onCancelClick={handleBindTechnologyOnCancelClick}
                onSuccess={handleOnTechKnowedgeCreationSuccess}
                chooseSkillLabel="Which tech have you used?"
                yearOfExposureLabel="What year did you start working with this skill?"
                monthsOfPracticeLabel="How many solid months of practice have you had since you were first exposed to the skill?"
              /> */}
            </div>
          </Modal>
        )}
      </section>
      <section className={`section section-divider`}>
        <ul className={`related-links`}>
          <li>
            <Link to="/submit-vacancy">Submit a vacancy &gt;&gt;</Link>
          </li>
          <li>
            <Link to="/employer/vacancies">Manage your vacancies &gt;&gt;</Link>
          </li>
        </ul>
      </section>
    </>
  );
}
