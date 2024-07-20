import { useLocation, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { mutateCreateTrans } from "../../tanstackqfns/mutate-create_trans";
import classes from "./FormCreateTrans.module.css";

import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import InputGroup from "../../components/inputs/InputGroup";
import Modal from "../../components/Modal";
import { useState } from "react";
import { queryTransaction } from "../../tanstackqfns/query-transaction";

const tranProcessingStatuses = {
  PROCESSING: "Processing, please wait",
  COMPLETED: "Completed",
  DECLINED: "Declined",
};


// const schema = (reservedUsernames) => z.object({
//   username: z.string()
//     .min(5, 'Username must be at least 5 characters long')
//     .nonempty('Username is required')
//     .refine(value => !reservedUsernames.includes(value), { message: 'This username is reserved' }),
//   age: z.number()
//     .min(18, 'Age must be at least 18')
//     .max(99, 'Age must be less than 100')
//     .int('Age must be an integer'),
// });


const schema = () => z.object({
  amount: z.string().min(1, "Amount is required").refine(value => {
    const parsed = parseFloat(value);
    return !isNaN(parsed) && parsed > 0;
  }, {
    message: 'Amount must be a number greater than 0',
  }),

});

export default function FormCreateTrans({
  buttonText,
  buttonTextSubmitting,
  mode,
}) {
  const [showModal, setShowModal] = useState(false);
  const [processingStatus, setProcessingStatus] = useState(
    tranProcessingStatuses.PROCESSING
  );

  const form = useForm({
    mode: "onBlur",
    resolver: zodResolver(schema()),
  });

  const mutationDeposit = useMutation({
    mutationFn: mutateCreateTrans,
    onSuccess: (data) => {
      pollTransactionStatus(data.data);
    },
    onError: (err) => {
      const serverValErrs = buildServerValErrs(err);
    },
  });

  function pollTransactionStatus(data) {
    const checkTranStatus = async () => {
      try {
        const res = await queryTransaction({ id: data.id });
        let tran = res.data;
        if (tran.status === 2) {
          setProcessingStatus(tranProcessingStatuses.COMPLETED);
        } else if (tran.status === 3) {
          setProcessingStatus(tranProcessingStatuses.DECLINED);
        } else {
          setTimeout(checkTranStatus, 5000);
          setProcessingStatus(tranProcessingStatuses.PROCESSING);
        }
      } catch (err) {
      } finally {
      }
    };

    checkTranStatus();
  }

  const serverValErrs = buildServerValErrs(mutationDeposit.error);

  function handleOnSubmit(data) {
    setProcessingStatus(tranProcessingStatuses.PROCESSING);
    setShowModal(true);

    let submissionData = {
      ...data
    }
    if(mode === "DEPOSIT") {
    }
    else if(mode === "WITHDRAW") {
      submissionData.amount *= -1
    }

    mutationDeposit.mutate({
      payload: submissionData,
    });
  }

  function handleCloseClick() {
    setShowModal(false);
    form.reset()
  }

  function handleOKClick() {
    setShowModal(false);
    form.reset()
  }

  return (
    <>
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

      {showModal && (
        <Modal onClose={handleCloseClick} show={showModal}>
          <div className={`form-container`}>
            <h2 className={`form-title`}>{processingStatus}</h2>
            {processingStatus !== tranProcessingStatuses.PROCESSING && (
              <button onClick={handleOKClick}>OK</button>
            )}
          </div>
        </Modal>
      )}
    </>
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
