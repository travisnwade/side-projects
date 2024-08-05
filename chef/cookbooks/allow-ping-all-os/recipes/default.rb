# recipes/default.rb

case node['platform']
when 'windows'
  template 'C:\\windows_firewall_rule.xml' do
    source 'windows_firewall_rule.xml.erb'
  end

  execute 'Enable ICMP (Ping) in Windows Firewall' do
    command 'netsh advfirewall firewall add rule name="Allow ICMPv4-In" protocol=icmpv4:any,any dir=in action=allow'
    action :run
  end

when 'ubuntu', 'centos', 'redhat', 'amazon'
  template '/tmp/linux_firewall_rule.sh' do
    source 'linux_firewall_rule.sh.erb'
    mode '0755'
  end

  execute 'Allow ICMP (Ping) in Linux Firewall' do
    command '/tmp/linux_firewall_rule.sh'
    action :run
  end
end
