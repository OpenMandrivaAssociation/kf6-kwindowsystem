%define major %(echo %{version} |cut -d. -f1-2)
%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)

%define libname %mklibname KF6WindowSystem
%define devname %mklibname KF6WindowSystem -d
#define git 20240217

Name: kf6-kwindowsystem
Version: 6.11.0
Release: %{?git:0.%{git}.}1
%if 0%{?git:1}
Source0: https://invent.kde.org/frameworks/kwindowsystem/-/archive/master/kwindowsystem-master.tar.bz2#/kwindowsystem-%{git}.tar.bz2
%else
Source0: http://download.kde.org/%{stable}/frameworks/%{major}/kwindowsystem-%{version}.tar.xz
%endif
Summary: Access to the windowing system
URL: https://invent.kde.org/frameworks/kwindowsystem
License: CC0-1.0 LGPL-2.0+ LGPL-2.1 LGPL-3.0
Group: System/Libraries
BuildRequires: cmake
BuildRequires: cmake(ECM)
BuildRequires: python
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QmlTools)
BuildRequires: cmake(Qt6Qml)
BuildRequires: cmake(Qt6GuiTools)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6DBusTools)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: cmake(WaylandProtocols)
BuildRequires: cmake(PlasmaWaylandProtocols)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: doxygen
BuildRequires: cmake(Qt6ToolsTools)
BuildRequires: cmake(Qt6)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-icccm)
BuildRequires: pkgconfig(xcb-xfixes)
BuildRequires: pkgconfig(xfixes)
Requires: %{libname} = %{EVRD}
Requires: %{name}-backend = %{EVRD}
Requires: (%{name}-backend-wayland = %{EVRD} if plasma6-kwin-wayland)
Requires: (%{name}-backend-x11 = %{EVRD} if x11-server-xorg)

%description
Access to the windowing system

%package -n %{libname}
Summary: Access to the windowing system
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Access to the windowing system

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Access to the windowing system

%package backend-wayland
Summary: Wayland backend for %{name}
Group: System/Libraries
Requires: %{libname} = %{EVRD}
Provides: %{name}-backend = %{EVRD}

%description backend-wayland
Wayland backend for %{name}

%package backend-x11
Summary: X11 backend for %{name}
Group: System/Libraries
Requires: %{libname} = %{EVRD}
Provides: %{name}-backend = %{EVRD}

%description backend-x11
X11 backend for %{name}

%prep
%autosetup -p1 -n kwindowsystem-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang %{name} --all-name --with-qt --with-html

%files -f %{name}.lang
%{_datadir}/qlogging-categories6/kwindowsystem.*
%dir %{_qtdir}/plugins/kf6
%dir %{_qtdir}/plugins/kf6/kwindowsystem
%{_qtdir}/qml/org/kde/kwindowsystem

%files backend-wayland
%{_qtdir}/plugins/kf6/kwindowsystem/KF6WindowSystemKWaylandPlugin.so

%files backend-x11
%{_qtdir}/plugins/kf6/kwindowsystem/KF6WindowSystemX11Plugin.so

%files -n %{devname}
%{_includedir}/KF6/KWindowSystem
%{_libdir}/cmake/KF6WindowSystem
%{_qtdir}/doc/KF6WindowSystem.*
%{_libdir}/pkgconfig/KF6WindowSystem.pc

%files -n %{libname}
%{_libdir}/libKF6WindowSystem.so*
