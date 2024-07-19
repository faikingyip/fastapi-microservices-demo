// import FormAddSkillExp from "../forms/FormAddSkillExp";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

// import LiSkill from "../list-item/LiSkill";
import classes from "./PageMicroservicesDemo.module.css";
import Modal from "../../components/Modal";
import { queryAccount } from "../../tanstackqfns/query-account";
import FormCreateTrans from "../forms/FormCreateTrans";

export default function PageMicroservicesDemo() {
  const [showModal, setShowShowModal] = useState(false);

  const accountUseQuery = useQuery({
    queryKey: ["account"],
    queryFn: queryAccount,
    staleTime: 10000,
  });

  function handleOnCloseModal() {
    setShowShowModal(false);
  }

  let contentAccountBindings;

  if (accountUseQuery.isPending) {
    contentAccountBindings = <div>Loading...</div>;
  }

  if (accountUseQuery.isError) {
  }

  if (accountUseQuery.isSuccess) {
    contentAccountBindings = <div>{accountUseQuery.data.data.balance}</div>;
  }

  return (
    <>
      <hr />
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Balance
        </h2>
        <div className={`${classes["balance"]}`}>
          {contentAccountBindings}
        </div>

      </section>
      
      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Deposit funds
        </h2>
        <div>
          <FormCreateTrans buttonText="Deposit" buttonTextSubmitting="Depositing" mode="DEPOSIT" />
        </div>
      </section>

      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Withdraw funds
        </h2>
        <div>
          <FormCreateTrans buttonText="Withdraw" buttonTextSubmitting="Withdrawing" mode="WITHDRAW" />
        </div>
      </section>

        {showModal && (
          <Modal onClose={handleOnCloseModal}>
            <div className={`form-container`}>
              <h2 className={`form-title`}>Add a tech experience</h2>
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
    </>
  );
}
