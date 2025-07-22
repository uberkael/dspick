# dspick.fish

function __dspick
    set script_dir (dirname (readlink -f (status --current-filename)))
    set input (commandline)
    set output (cd $script_dir; echo $input | uv run dspick.py)
    commandline --replace "$output"
end

bind \cg '__dspick'
