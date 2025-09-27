set -e

load_env() {
    if [ -f ".env"]; then
      source.env
      echo "loaded config from env"

      required_vars=("KADEMIA_ID", "KADEMIA_PASSWORD", "SCRIPT_PATH")
      for var in "${required_vars[@]}"; do
          if [ -z "${!var}" ]; then
               echo "Required environment variable $var is not set in .env file"
                exit 1
            fi
          done
    else
      echo ".env file not found!"
        exit 1
    fi


}

check_python_scripts() {
    echo "Checking for bootstrap script..."

    if [ ! -f "SCRIPT_PATH" ]; then
        echo "user bootstrap not found at SCRIPT_PATH"
        exit 1
    fi


}


main(){
  load_env
  check_python_scripts
}