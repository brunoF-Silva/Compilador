fun a1(int a) { return a * 2.3; }
fun a2(int b) { return b / 2; }

print a1(4) * a2(10);
print a2(5) / a1(50);
float c = 5.8;
if (a1(4) > 5)
{
  print "ok";
}
c = 40.2;
print c;