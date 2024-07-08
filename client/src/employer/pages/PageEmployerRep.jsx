import { useQuery } from "@tanstack/react-query";
import { queryEmployerRep } from "../../tanstackqfns/query-employer-rep";
import { Link } from "react-router-dom";
import DetailDisplayText from "../detail/DetailDisplayText";
import { z } from "zod";
import { mutatePatchEmployerRep } from "../../tanstackqfns/mutate-patch-employer-rep";

export default function PageEmployerRep() {
  const queryKey = ["employer-rep"];

  const employerRepQuery = useQuery({
    queryKey: queryKey,
    queryFn: queryEmployerRep,
    staleTime: 1000 * 60 * 5,
  });

  let content;
  if (employerRepQuery.isLoading) {
    content = <div>Loading...</div>;
  }

  if (employerRepQuery.isError) {
    throw employerRepQuery.error;
  }

  let isAllDetailsProvided = false;

  if (employerRepQuery.data) {
    isAllDetailsProvided = !Object.values(employerRepQuery.data.data).some(
      (val) => !val
    );
    const empRep = employerRepQuery.data.data;
    content = (
      <ul>
        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="company_name"
            fieldTitle="Company name"
            fieldValue={empRep.company_name}
            zodSchema={z.object({
              company_name: z.string().optional(),
            })}
            mutationFn={mutatePatchEmployerRep}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>

        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="company_number"
            fieldTitle="Company number"
            fieldValue={empRep.company_number}
            zodSchema={z.object({
              company_number: z.string().optional(),
            })}
            mutationFn={mutatePatchEmployerRep}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>

        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="job_title"
            fieldTitle="Job title"
            fieldValue={empRep.job_title}
            zodSchema={z.object({
              job_title: z.string().optional(),
            })}
            mutationFn={mutatePatchEmployerRep}
            queriesToInvalidateOnSuccess={queryKey}
          />
          <hr />
        </li>

        <li className={`list-item`}>
          <DetailDisplayText
            fieldName="contact_number"
            fieldTitle="Contact number"
            fieldValue={empRep.contact_number}
            zodSchema={z.object({
              contact_number: z.string().optional(),
            })}
            mutationFn={mutatePatchEmployerRep}
            queriesToInvalidateOnSuccess={queryKey}
          />
        </li>
      </ul>
    );
  }

  return (
    <>
      <hr />
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Your employer profile
        </h2>
        <p className={`section-text`}>
          Build your employer profile so you can tell us about a vacancy.
        </p>

        <div className={`section-body`}>{content}</div>
      </section>
      <section className={`section section-divider`}>
        <ul className={`related-links`}>
          <li>
            {!isAllDetailsProvided && (
              <span className={`disabled-link`}>Submit a vacancy &gt;&gt;</span>
            )}
            {isAllDetailsProvided && (
              <Link to="/submit-vacancy">Submit a vacancy &gt;&gt;</Link>
            )}
          </li>
          <li>
            <Link to="/employer/vacancies">Manage your vacancies &gt;&gt;</Link>
          </li>
        </ul>
      </section>
    </>
  );
}
