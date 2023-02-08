#SingleInstance force

CoordMode, Pixel, Screen
CoordMode, Mouse, Screen
CoordMode, Tooltip, Screen
CoordMode, ImageSearch, Screen

clipboard := "https://search.arxiv.org/?query=aerospace&qid=1675860280485ler_nCnN_1505998205&startat="

Sleep, 3000
index := 0

Loop, 37 {
	global index
	SaveCurrentPage(index)
	index := index + 10
	NextPage(index)
}

NextPage(index) {
	Send, !{d}
	Sleep, 500
	Send, ^{v}
	Send, %index%
	Sleep, 500
	Send, {enter}
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
