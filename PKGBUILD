# Maintainer: Frans-Willem Hardijzer <fw@hardijzer.nl>

pkgname=gandi-update
pkgver=2015.12.24
pkgrel=1
pkgdesc="Automatically update Gandi subdomain with external IP"
arch=('i686' 'x86_64')
url="http://github.com/Frans-Willem/GandiUpdate"
license=('Proprietary')
makedepends=()
source=()
md5sums=()
install=GandiUpdate.install

package() {
cd "${srcdir}/../"
	install -d -m755 "${pkgdir}/usr/local/bin"
	install -d -m755 "${pkgdir}/usr/lib/systemd/system"
	install -d -m755 "${pkgdir}/etc/sysconfig"
	install -D -m755 GandiUpdate.py "${pkgdir}/usr/local/bin/"
	install -D -m644 GandiUpdate.timer "${pkgdir}/usr/lib/systemd/system/"
	install -D -m644 GandiUpdate.service "${pkgdir}/usr/lib/systemd/system/"
	install -D -m600 GandiUpdate.config "${pkgdir}/etc/sysconfig/GandiUpdate"
}
