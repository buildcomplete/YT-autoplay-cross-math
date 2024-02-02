filename = resultFilename;
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

fdisp(fid, "fieldCenters_r=");
fdisp(fid, fieldCenters_r+ p_b(1));
fdisp(fid, "fieldCenters_c=");
fdisp(fid, fieldCenters_c + p_b(2));

fdisp(fid, "varCenters_r=");
fdisp(fid, varRowIdx+ v_b(1));
fdisp(fid, "varCenters_c=");
fdisp(fid, varColIdx + v_b(2));

fclose (fid);
