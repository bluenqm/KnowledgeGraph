#SingleInstance force

CoordMode, Pixel, Screen
CoordMode, Mouse, Screen
CoordMode, Tooltip, Screen
CoordMode, ImageSearch, Screen

; https://ntrs.nasa.gov/collections/pubspace?stiTypeDetails=Accepted%20Manuscript%20(Version%20with%20final%20changes)&page=%7B%22size%22:100,%22from%22:0%7D

Sleep, 3000
index := 1

Loop, 47 {
	SaveCurrentPage(index)
	index := index + 1
	NextPage()
}

NextPage() {
	MouseClick, left, 1675, 255
	Sleep, 10000
}

SaveCurrentPage(name) {
	Send, ^{s}
	Sleep, 1000
	Send, %name%
	Sleep, 1000
	Send, {enter}
	Sleep, 4000
}

$esc::
{
	exitapp
}
