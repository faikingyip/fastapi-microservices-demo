import { useState } from "react";
import Modal from "../../components/Modal";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { mutateDeleteTechKnowledge } from "../../tanstackqfns/mutate-delete-tech-knowledge";
import classes from "./LiSkill.module.css";

export default function LiSkill({
  id,
  skillName,
  yearFirstExposed,
  monthsPractice,
}) {
  const [isDeleting, setIsDeleting] = useState(false);
  const queryClient = useQueryClient();
  const deleteMutation = useMutation({
    mutationFn: mutateDeleteTechKnowledge,
    // onMutate: (data) => {
    //   const id = data.id;

    //   queryClient.cancelQueries({ queryKey: ["tech-knowledge"] });
    //   const currentData = queryClient.getQueryData(["tech-knowledge"]);
    //   let newData = JSON.parse(JSON.stringify(currentData));
    //   newData.data.results = newData.data.results.filter(
    //     (item) => item.id !== id
    //   );
    //   newData.data.count = newData.data.results.length;
    //   queryClient.setQueryData(["tech-knowledge"], newData);
    //   setIsDeleting(false);
    // },
    onSuccess: () => {
      queryClient.invalidateQueries(["tech-knowledge"]);
      setIsDeleting(false);
    },
  });

  function handleOnStartDelete(e) {
    setIsDeleting(true);
  }

  function handleOnStopDelete(e) {
    setIsDeleting(false);
  }

  function handleOnConfirmDelete(e) {
    deleteMutation.mutate({
      id: id,
    });
  }

  return (
    <>
      {isDeleting && (
        <Modal onClose={handleOnStopDelete}>
          <div className={`form-container`}>
            <h2 className={`form-title form-title-color-standard`}>
              Are you sure?
            </h2>
            <p className={`form-prompt`}>
              Confirm you wish to remove{" "}
              <span className={`emphasis`}>{skillName}</span> from your listed
              experiences.
            </p>

            <div className={`${classes["buttons"]}`}>
              <button
                type="button"
                disabled={deleteMutation.isPending}
                onClick={handleOnStopDelete}
                className={`button button-color-cancel`}
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={deleteMutation.isPending}
                onClick={handleOnConfirmDelete}
                className={`button button-color-alert`}
              >
                {deleteMutation.isPending ? "Deleing" : "Delete"}
              </button>
            </div>
          </div>
          {/* {isErrorDeleting && (
            <ErrorBlock
              title="Failed to delete event"
              message={
                deleteError.info?.message ||
                "Failed to delete event, please try again later."
              }
            />
          )} */}
        </Modal>
      )}
      <div className={`${classes["skill-detail"]}`}>
        <div className={`${classes["skill-heading"]}`}>
          <h3 className={`${classes["skill-name"]}`}>{skillName}</h3>
          <button
            type="button"
            onClick={handleOnStartDelete}
            className={`button button-color-alert ${classes.button}`}
          >
            Remove
          </button>
        </div>
        <span className={`${classes["skill-label"]}`}>First exposure in</span>
        <span className={`${classes["skill-value"]}`}>{yearFirstExposed}</span>
        <span className={`${classes["skill-label"]}`}>with</span>
        <span className={`${classes["skill-value"]}`}>{monthsPractice}</span>
        <span className={`${classes["skill-label"]}`}>months of practice.</span>
        <div className="skill-level">
          <span className={`${classes["skill-label"]}`}>Skill level</span>
          <span className={`${classes["skill-value"]}`}>To be assessed</span>
        </div>
      </div>
    </>
  );
}