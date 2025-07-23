#!/usr/bin/env fish
set --global __dspick_dir (dirname (readlink -f (status --current-filename)))

function __dspick
    set --local input (commandline --current-process | string trim)

    if test -n "$input"
        set --local output (echo $input | uv run $__dspick_dir/dspick.py 2>/dev/null | string trim)

        if test -n "$output"
            commandline --current-process $output
        end
    end
end

bind \cg __dspick
bind --mode insert \cg __dspick
