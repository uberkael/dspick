function _dspick_replace
    set --local input (commandline --current-process | string trim)

    if test -n "$input"
        set --local script_dir (dirname (readlink -f (status --current-filename)))
        set --local output (echo $input | uv run $script_dir/dspick.py 2>/dev/null | string trim)

        if test -n "$output"
            commandline --current-process $output
        end
    end
end

bind \cg _dspick_replace
bind --mode insert \cg _dspick_replace
