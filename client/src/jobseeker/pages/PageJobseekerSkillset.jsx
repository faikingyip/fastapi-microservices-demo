import FormAddSkillExp from "../forms/FormAddSkillExp";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { queryTechs } from "../../tanstackqfns/query-techs";
import { queryTechKnowledge } from "../../tanstackqfns/query-tech-knowledge";
import LiSkill from "../list-item/LiSkill";
import classes from "./PageJobseekerSkillset.module.css";
import Modal from "../../components/Modal";

export default function PageJobseekerSkillset() {
  const [showBindTechnologyForm, setShowBindTechnologyForm] = useState(false);

  const { data: techs } = useQuery({
    queryKey: ["techs"],
    queryFn: queryTechs,
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 5, // 5 minutes
  });

  const {
    data: techKnowledge,
    isPending: isPendingTechKnowledge,
    isSuccess: isSuccessTechKnowledge,
    isError: isErrorTechKnowledge,
  } = useQuery({
    queryKey: ["tech-knowledge"],
    queryFn: queryTechKnowledge,
    staleTime: 10000,
  });

  function handleShowBindTechnologyFormOnClick() {
    setShowBindTechnologyForm(true);
  }

  function handleBindTechnologyOnCancelClick() {
    setShowBindTechnologyForm(false);
  }

  function handleOnTechKnowedgeCreationSuccess() {
    setShowBindTechnologyForm(false);
  }

  let contentTechKnowledgeBindings;

  if (isPendingTechKnowledge) {
    contentTechKnowledgeBindings = <div>Loading...</div>;
  }

  if (isErrorTechKnowledge) {
  }

  if (isSuccessTechKnowledge) {
    contentTechKnowledgeBindings = (
      <ul>
        {techKnowledge.data.results.map((item, index) => {
          return (
            <li key={item.id} className={`${classes["tech-knowledge-item"]}`}>
              <LiSkill
                id={item.id}
                skillName={item.tech.name}
                yearFirstExposed={item.year_of_first_exposure}
                monthsPractice={item.months_of_practice}
              />
              {index < techKnowledge.data.results.length - 1 && <hr />}
            </li>
          );
        })}
      </ul>
    );
  }

  return (
    <>
      <hr />
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Techs you have used
        </h2>
        <div className={`${classes["tech-bindings"]}`}>
          {contentTechKnowledgeBindings}
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
              <h2 className={`form-title`}>Add a tech experience</h2>
              <FormAddSkillExp
                skills={techs.data}
                onCancelClick={handleBindTechnologyOnCancelClick}
                onSuccess={handleOnTechKnowedgeCreationSuccess}
                chooseSkillLabel="Which tech have you used?"
                yearOfExposureLabel="What year did you start working with this skill?"
                monthsOfPracticeLabel="How many solid months of practice have you had since you were first exposed to the skill?"
              />
            </div>
          </Modal>
        )}
      </section>
      {/* <section id="concepts">
        <h2>Which of the following have you practiced?</h2>
      </section> */}
    </>
  );
}
