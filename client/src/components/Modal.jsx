import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";
import classes from "./Modal.module.css";

export default function Modal({ children, onClose, show }) {
  const dialog = useRef();

  useEffect(() => {
    // Using useEffect to sync the Modal component with the DOM Dialog API
    // This code will open the native <dialog> via it's built-in API whenever the <Modal> component is rendered
    if (show) {
      dialog.current.showModal();
    } else {
      dialog.current.close();
    }
  }, [show]);

  return createPortal(
    <dialog className={`${classes.modal}`} ref={dialog} onClose={onClose}>
      {children}
    </dialog>,
    document.getElementById("modal")
  );
}
