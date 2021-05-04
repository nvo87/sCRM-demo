#/bin/bash

source_it() {
  while read -r line; do
    if [[ -n "$line" ]] && [[ $line != \#* ]]; then
      export "$line"
    fi
  done < $1
}

for f in .local/*.env; do
  source_it $f
done
