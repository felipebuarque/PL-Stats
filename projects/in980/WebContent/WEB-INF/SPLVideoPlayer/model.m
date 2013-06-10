SPLVideoPlayer : OperatingSystem ControlOutboundStreaming VideoFormat+ AudioFormat+ ProtocolCapabilities+ Repetition OnLineManagement* [ControlPanel] OpticalMediaCapabiltyy AdvancedManagement* PlaylistManagement :: _SPLVideoPlayer ;

OperatingSystem : Windows
	| Linux ;

ControlOutboundStreaming : aaa :: _ControlOutboundStreaming ;

VideoFormat : MPEG_1
	| MPEG_2
	| MPEG_4
	| RealVideo
	| WMV
	| Flash ;

AudioFormat : MP3
	| WMA
	| RealAudio
	| Vorbis
	| APE ;

ProtocolCapabilities : HTTP
	| HTTPS
	| FTP ;

Repetition : Playlist Track :: _Repetition ;

OnLineManagement : MediaDatabase
	| OnlineBookmark ;

ControlPanel : Visualizer Skinnable :: _ControlPanel ;

OpticalMediaCapabiltyy : AudioMedia VideoMedia :: _OpticalMediaCapabiltyy ;

AudioMedia : CD DVD :: _AudioMedia ;

VideoMedia : VCD SVCD BlueRay :: _VideoMedia ;

AdvancedManagement : TimeStretching
	| PitchShifting
	| ABRepeat
	| AudioResync
	| SubtitleResync ;

PlaylistManagement : SortPlaylist PlaylistFormatCapability Shuffle SmartPlaylist :: _PlaylistManagement ;

PlaylistFormatCapability : M3U ASX PLS XSPF :: _PlaylistFormatCapability ;

%%

MediaDatabase implies ProtocolCapabilities ;

