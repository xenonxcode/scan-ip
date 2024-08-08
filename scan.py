import subprocess
import csv
import sys

def ping_ip_list(ip_list, output_file):
    active_ips = []
    inactive_ips = []


    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Address', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()

        for ip in ip_list:
            print(f"Pinging {ip}...")

            result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if "Reply dari" in result.stdout.decode('utf-8'):
                active_ips.append(ip)
                writer.writerow({'Address': ip, 'Status': 'Active'})
                print(f"{ip} active")
            else:
                inactive_ips.append(ip)
                writer.writerow({'Address': ip, 'Status': 'Inactive'})
                print(f"{ip} tidak active")

    return active_ips, inactive_ips

def read_ip_list_from_csv(file_path):
    ip_list = []
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            if 'Address' not in reader.fieldnames:
                print("Error: 'Address' column tidak ada di CSV file.")
                sys.exit(1)
            
            for row in reader:
                ip_list.append(row['Address'])
    except FileNotFoundError:
        print(f"Error: File {file_path} tidak ada.")
        sys.exit(1)
    except Exception as e:
        print(f"Kesalahan: {e}")
        sys.exit(1)
        
    return ip_list

def main():
    if len(sys.argv) < 2:
        print("Cara Pakai: python scan.py <input_csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    ip_list = read_ip_list_from_csv(input_file)

    output_file = "ip_scan_results.csv"

    active_ips, inactive_ips = ping_ip_list(ip_list, output_file)
    print("Active IPs:", active_ips)
    print("Inactive IPs:", inactive_ips)
    print(f"Result disimpan di {output_file}")

if __name__ == "__main__":
    main()
