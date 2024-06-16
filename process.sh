#!/bin/bash

# folder where the html pages and audio files are kept
# SET THIS VARIABLE 
site_dir='~/Jpn_scripts'

eval exp_site_dir="$site_dir"

# Python command
python_cmd=""
if [[ "$(uname)" == "Darwin" ]]; then
	# macOS
	python_cmd="python3"
else
	python_cmd="python"
fi

mkdir -p ${exp_site_dir}/pages
mkdir -p ${exp_site_dir}/audio

remove_extension() {
	local filename=$1
	local mov_name=${filename%.*}
	echo "$mov_name"
} 

get_filename() {
	local filepath=$1
	echo $(remove_extension $(echo $(basename $1)))
}

get_extension() {
	local filepath=$1
	echo $(basename $1 | grep -o '\..*$')
}

create_page() {
	if [ -z "$mov_file" ]; then
		# in case no movie file is provided, the movie title is extracted from
		# the subtitle filename 
		$python_cmd create_page.py "$sub_file" > \
			"${exp_site_dir}/pages/${mov_title}.html"
	else
		extract_audio
		$python_cmd create_page.py "$sub_file" \
		"${exp_site_dir}/audio/${mov_title}.mp3" > \
				"${exp_site_dir}/pages/${mov_title}.html"
	fi
}

extract_audio() {
	# Extract audio, convert to mono, and save as MP3 with a static bitrate
	ffmpeg -i "$mov_file" -map 0:a:$track_n -vn -acodec libmp3lame \
		-ac 1 -ab 64k "${exp_site_dir}/audio/${mov_title}.mp3"
}

process_file() {
	local filepath=$1
	local extension=$(get_extension $filepath)
	if [ "$extension" = ".ass" ]; then
		# call python script	
		sub_file=$filepath
		mov_title=$(get_filename $filepath)
	elif [ "$extension" = '.mkv' ]; then
		mov_file=$filepath
		mov_title=$(get_filename $filepath)
	fi
}

while [[ "$1" != "" ]]; do
	case $1 in
		-a | --audio-track)
			shift
			track_n=$1
			;;
		* )
			if [ -f $1 ]; then
				process_file $1	
			else
				echo "Unknown option: $1"
				exit 1
			fi
			;;
	esac
	shift
done

create_page 

