#!/usr/bin/env bash

file="$1"

mime=$(file --mime-type -Lb "$file")

is_dir() {
	[ -d "$file" ]
}

is_image() {
	[[ "$mime" == image/* ]]
}

is_pdf() {
	[[ "$mime" == application/pdf ]]
}

is_video() {
	[[ "$mime" == video/* ]]
}

is_archive() {
	[[ "$mime" == application/zip ]] ||
		[[ "$file" == *.tar ]] ||
		[[ "$file" == *.tar.gz ]] ||
		[[ "$file" == *.tgz ]] ||
		[[ "$file" == *.rar ]] ||
		[[ "$file" == *.7z ]]
}

preview_image() {
	local cols="${FZF_PREVIEW_COLUMNS:-$(tput cols)}"
	local lines="${FZF_PREVIEW_LINES:-$(tput lines)}"
	chafa --format=symbols --symbols=block+border --color-space=din99d \
		--color-extractor=average --work=9 \
		--size="${cols}x${lines}" "$file"
}

preview_pdf() {
	# conversión ligera de primeras páginas
	pdftotext -l 5 "$file" - 2>/dev/null | bat --language=txt --style=numbers --color=always
}

preview_video() {
	if command -v ffmpegthumbnailer >/dev/null 2>&1; then
		tmp="/tmp/fzf-video-thumb.jpg"
		ffmpegthumbnailer -i "$file" -o "$tmp" -s 0 2>/dev/null
		if [ -f "$tmp" ]; then
			local cols="${FZF_PREVIEW_COLUMNS:-$(tput cols)}"
			local lines="${FZF_PREVIEW_LINES:-$(tput lines)}"
			chafa --format=symbols --symbols=block+border --color-space=din99d \
				--color-extractor=average --work=9 \
				--size="${cols}x${lines}" "$tmp"
		fi
	fi

	# fallback info útil
	ffprobe -v error -show_format -show_streams "$file" 2>/dev/null | head -n 40
}

preview_archive() {
	case "$file" in
	*.zip)
		unzip -l "$file" 2>/dev/null | sed -n '1,100p'
		;;
	*.tar | *.tar.gz | *.tgz)
		tar -tf "$file" 2>/dev/null | sed -n '1,100p'
		;;
	*.rar)
		unrar l "$file" 2>/dev/null | sed -n '1,100p'
		;;
	*.7z)
		7z l "$file" 2>/dev/null | sed -n '1,100p'
		;;
	esac
}

# ---------------- MAIN ----------------

if is_dir "$file"; then
	eza --tree --level=2 --icons "$file"

elif is_image "$file"; then
	preview_image "$file"

elif is_pdf "$file"; then
	preview_pdf "$file"

elif is_video "$file"; then
	preview_video "$file"

elif is_archive "$file"; then
	preview_archive

else
	case "$mime" in
	text/* | application/json)
		bat --style=numbers --color=always "$file"
		;;
	*)
		file "$file"
		;;
	esac
fi
