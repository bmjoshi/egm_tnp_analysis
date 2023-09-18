echo $1 $2
cp index.php $1
dirlist=$(find $1 -maxdepth $2 -type d)
echo $dirlist
for d in $dirlist; do
   s=$(ls $d | grep index.php);
   if [[ s!="" ]]; then
      cp index.php $d;
   fi
done
