import { useQuery, useQueryClient } from "@tanstack/react-query";
import { queryEmployerRep } from "../../tanstackqfns/query-employer-rep";
import { Link, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import classes from "./PageSubmitVacancy.module.css";
import FormCreateVacancy from "../forms/FormCreateVacancy";

export default function PageSubmitVacancy() {
  const queryClient = useQueryClient();

  const employerRepQuery = useQuery({
    queryKey: ["employer-rep"],
    queryFn: queryEmployerRep,
    staleTime: 1000 * 60 * 5,
  });

  const navigate = useNavigate();

  useEffect(() => {
    if (employerRepQuery.data) {
      const data = employerRepQuery.data.data;
      if (Object.values(employerRepQuery.data.data).some((val) => !val)) {
        navigate("/build-employer-profile");
      }
    }
  }, [employerRepQuery.data]);

  let content;
  if (employerRepQuery.isLoading) {
    content = <div>Loading...</div>;
  }

  if (employerRepQuery.isError) {
    throw employerRepQuery.error;
  }

  if (employerRepQuery.data) {
    content = <div>{employerRepQuery.data.data.user}</div>;
  }

  return (
    <>
      <hr />
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Tell us about a vacancy
        </h2>

        <FormCreateVacancy />
      </section>
      <section className={`section section-divider`}>
        <ul className={`related-links`}>
          <li>
            <Link to="/build-employer-profile">
              View your employer profile &gt;&gt;
            </Link>
          </li>
          <li>
            <Link to="/employer/vacancies">
              Manage your vacancies &gt;&gt;
            </Link>
          </li>
        </ul>
      </section>
    </>
  );
}
