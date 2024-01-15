filename = "cross-math-scan-result.txt";
fid = fopen (filename, "w");

fdisp(fid, "fieldTypes=");
fdisp(fid, size(fieldTypes));
fdisp(fid, fieldTypes);

fdisp(fid, "symbolsAtPositions=");
fdisp(fid, size(symbolsAtPositions,1));
fdisp(fid, symbolsAtPositions);

fdisp(fid, "variables_with_pos=");
fdisp(fid, size(variables_with_pos,1));
fdisp(fid, variables_with_pos);
fclose (fid);
