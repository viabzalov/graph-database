conda --version
if [[ $? -ne 0 ]]; then
  case "$OSTYPE" in
    linux*)  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh ;;
    darwin*) wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh ;;
  esac

  bash ./miniconda.sh -b -p $HOME/miniconda
  export PATH=$HOME/miniconda:$PATH
  source "$HOME/miniconda/etc/profile.d/conda.sh"
  hash -r
  conda init bash
  conda config --set always_yes yes --set changeps1 yes
  conda update -q conda
  # Useful for debugging issues with conda
  conda info -a
fi
conda config --add channels conda-forge
conda create -q -n test-environment python=3.8
conda activate test-environment || activate test-environment
conda install pygraphblas
export PYTHONPATH="${PYTHONPATH}:./"
pip3 install --upgrade pip
pip install -r requirements.txt
cd tests/benchmark_rpq/ ; gdown https://drive.google.com/uc?id=1ZZ8FI6MxQ2rWIRxBQjZOVw64zHdbxcmm ; cd ../../
rm -rf .benchmarks
pwd
sudo nice -n -20 python3 -m pytest -v -s tests/benchmark_rpq/test_benchmark_rpq.py --benchmark-autosave --benchmark-save-data &
pytest-benchmark compare --name=short --csv=RPQ
cat RPQ.csv