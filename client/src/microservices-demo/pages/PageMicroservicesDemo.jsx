// import FormAddSkillExp from "../forms/FormAddSkillExp";
import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";

// import LiSkill from "../list-item/LiSkill";
import classes from "./PageMicroservicesDemo.module.css";
import Modal from "../../components/Modal";
import { queryAccount } from "../../tanstackqfns/query-account";
import FormCreateTrans, { formModes } from "../forms/FormCreateTrans";

export default function PageMicroservicesDemo() {
  // const [showModal, setShowShowModal] = useState(false);
  const queryClient = useQueryClient();

  const accountUseQuery = useQuery({
    queryKey: ["account"],
    queryFn: queryAccount,
    staleTime: 10000,
  });

  // function handleOnCloseModal() {
  //   setShowShowModal(false);
  // }

  function onSubmissionCompleted() {
    queryClient.invalidateQueries({
      queryKey: ["account"],
    });
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
        <h2 className={`section-title section-title-color-wood`}>Balance</h2>
        <div className={`${classes["balance"]}`}>{contentAccountBindings}</div>
      </section>

      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Deposit funds
        </h2>
        <div>
          <FormCreateTrans
            onSubmissionCompleted={onSubmissionCompleted}
            buttonText="Deposit"
            buttonTextSubmitting="Depositing"
            mode={formModes.DEPOSIT}
          />
        </div>
      </section>

      <section className={`section`}>
        <h2 className={`section-title section-title-color-wood`}>
          Withdraw funds
        </h2>
        <div>
          <FormCreateTrans
            onSubmissionCompleted={onSubmissionCompleted}
            buttonText="Withdraw"
            buttonTextSubmitting="Withdrawing"
            mode={formModes.WITHDRAW}
          />
        </div>
      </section>

      {/* {showModal && (
        <Modal onClose={handleOnCloseModal}>
          <div className={`form-container`}>
            <h2 className={`form-title`}>Add a tech experience</h2>
          </div>
        </Modal>
      )} */}
    </>
  );
}
