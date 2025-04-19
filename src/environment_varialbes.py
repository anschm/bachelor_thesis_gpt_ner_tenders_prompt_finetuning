import os


def get_results_dir():
    """
    Retrieves the directory for storing results. If the environment variable
    'RESULTS_DIR' is set, its value is returned. Otherwise, it defaults to
    a subdirectory named 'tender-results' within the working directory.

    Returns:
        str: The path to the results directory.
    """
    results_dir = os.environ.get('RESULTS_DIR')
    if results_dir:
        return results_dir
    work_dir = get_work_dir()
    return os.path.join(work_dir, 'tender-results')


def get_test_data_dir():
    """
    Retrieves the directory for test data. If the environment variable
    'TEST_DATA_DIR' is set, its value is returned. Otherwise, it defaults to
    a subdirectory named 'tender-test-data' within the working directory.

    Returns:
        str: The path to the test data directory.
    """
    test_data_dir = os.environ.get('TEST_DATA_DIR')
    if test_data_dir:
        return test_data_dir

    work_dir = get_work_dir()
    return os.path.join(work_dir, 'tender-test-data')


def get_work_dir():
    """
    Retrieves the working directory. If the environment variable 'WORK_DIR' is
    set, its value is returned. Otherwise, it defaults to the current directory './'.

    Returns:
        str: The path to the working directory.
    """
    test_data_dir = os.environ.get('WORK_DIR')
    if not test_data_dir:
        return './'
    return test_data_dir


def get_openai_api_key():
    """
    Retrieves the OpenAI API key from the environment variable 'OPENAI_API_KEY'.
    If the variable is not set, it returns None, indicating the absence of a key.

    Returns:
        str | None: The OpenAI API key or None if not set.
    """
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        return None
    return openai_api_key


def get_openai_role():
    """
    Retrieves the OpenAI role from the environment variable 'OPENAI_ROLE'.
    If the variable is not set, it returns None, indicating the absence of a role.

    Returns:
        str | None: The OpenAI role or None if not set.
    """
    openai_role = os.environ.get('OPENAI_ROLE')
    if not openai_role:
        return None
    return openai_role


def get_openai_model():
    """
    Retrieves the OpenAI model from the environment variable 'OPENAI_MODEL'.
    If the variable is not set, it returns None, indicating the absence of a model.

    Returns:
        str | None: The OpenAI model or None if not set.
    """
    openai_model = os.environ.get('OPENAI_MODEL')
    if not openai_model:
        return None
    return openai_model
