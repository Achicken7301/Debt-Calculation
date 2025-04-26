Attribute VB_Name = "Module1"
Sub MarkHorizontalPageBreaks_InsideLine()
    Dim ws As Worksheet
    Dim hBreak As HPageBreak
    Dim breakRow As Long
    Dim lastCol As Long
    Dim msg As String

    Set ws = ActiveSheet
    lastCol = 5

    msg = "Drawing horizontal lines between rows at each page break:" & vbCrLf & vbCrLf

    For Each hBreak In ws.HPageBreaks
        breakRow = hBreak.Location.Row

        ' Draw inside horizontal border between breakRow - 1 and breakRow
        With ws.Range(ws.Cells(breakRow - 1, 1), ws.Cells(breakRow, lastCol)).Borders(xlInsideHorizontal)
            .LineStyle = xlContinuous
            .Weight = xlMedium
            .Color = RGB(0, 0, 0)
        End With

        msg = msg & "Line drawn between row " & breakRow - 1 & " and " & breakRow & vbCrLf
    Next hBreak

    MsgBox msg, vbInformation, "Page Break Lines Drawn"
End Sub

