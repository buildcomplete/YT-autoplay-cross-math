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
fprintf(fid, '%d ', fieldCenters_r + p_b(1));
fprintf(fid, '\n');  % Add a newline after each row

fdisp(fid, "fieldCenters_c=");
fprintf(fid, '%d ', fieldCenters_c + p_b(2));
fprintf(fid, '\n');  % Add a newline after each row

fdisp(fid, "varCenters_r=");
fprintf(fid, '%d ',varRowIdx+ v_b(1));
fprintf(fid, '\n');  % Add a newline after each row

fdisp(fid, "varCenters_c=");
fprintf(fid, '%d ', varColIdx + v_b(2));
fprintf(fid, '\n');  % Add a newline after each row


fclose (fid);
