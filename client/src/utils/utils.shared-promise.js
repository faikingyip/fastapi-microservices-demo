/**
 * Wraps the specified async function to allow two or
 * more callers to await the same promise,
 * for authentication data. For example, if you need to
 * refresh the jwt access token using the refresh token
 * and if multiple callers are making the call, then wrapping
 * the function is particularly useful as it will return
 * the same instance of the promise to each caller.
 */
const configureSharedPromise = (func) => {
  let sharedPromise = null;

  async function wrapper() {
    if (!sharedPromise) {
      sharedPromise = new Promise(async (resolve, reject) => {
        try {
          const result = await func();
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          sharedPromise = null;
        }
      });
    }
    return sharedPromise;
  }
  return wrapper;
};

export default configureSharedPromise;
