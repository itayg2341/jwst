import re

file_path = 'jwst/extract_1d/soss_extract/atoca_utils.py'

with open(file_path, 'r') as f:
    content = f.read()

old_function_pattern = r"""def try_solve_two_methods\(matrix, result\):.*?return lsqr\(matrix, result\)\[0\]"""

new_function = """def try_solve_two_methods(matrix, result):
    \"\"\"
    Solve sparse matrix equation A.x=b, reverting to least-squared solver when spsolve fails.

    On rare occasions spsolve's approximation of the matrix is not appropriate
    and fails on good input data.

    Parameters
    ----------
    matrix : array-like
        Matrix A in the system to solve A.x = b
    result : array-like
        Vector b in the system to solve A.x = b

    Returns
    -------
    array
        Solution x of the system (1d array)
    \"\"\"
    with warnings.catch_warnings():
        warnings.filterwarnings(action="error", category=MatrixRankWarning)
        try:
            return spsolve(matrix, result)
        except MatrixRankWarning:
            log.info("ATOCA matrix solve failed with spsolve. Retrying with least-squares.")
            try:
                return lsqr(matrix, result)[0]
            except Exception:
                log.warning("ATOCA matrix solve failed with least-squares.", exc_info=True)
                return np.full(matrix.shape[1], np.nan)"""

# Use re.sub with re.DOTALL to handle multiline patterns
new_content = re.sub(old_function_pattern, new_function, content, flags=re.DOTALL)

with open(file_path, 'w') as f:
    f.write(new_content)
