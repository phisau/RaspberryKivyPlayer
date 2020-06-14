import subprocess
import re
command = ['ping', '-c', '1', '192_168_1_1']
output = subprocess.check_output(command)

output_192_168_1_1 = re.search(r'1 packets .*',output.decode('UTF-8'))
package_loss = output_192_168_1_1.group(0).split(',')[2].strip().split('%')[0].strip()
print(package_loss)
if package_loss == '0':
    print('erreichbar')
elif package_loss == '100':
    print('nicht erreichbar')
else:
    print("langsame Verbindung")
print(output_192_168_1_1)
