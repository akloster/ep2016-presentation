// Generated by CoffeeScript 1.10.0
(function() {
  define('binaural', [], function() {
    var BinauralBeat, binauralComm, binauralSet, binauralStop;
    BinauralBeat = (function() {
      function BinauralBeat(left1, right1, gainLeft1, gainRight1, duration1) {
        var audioCtx, gain1, gain2, merger, oscillator1, oscillator2, silence, stopTime;
        this.left = left1;
        this.right = right1;
        this.gainLeft = gainLeft1;
        this.gainRight = gainRight1;
        this.duration = duration1;
        audioCtx = window.binauralAudioCtx;
        this.audioCtx = audioCtx;
        console.log("duration", this.duration);
        oscillator1 = audioCtx.createOscillator();
        oscillator1.frequency.value = this.left;
        gain1 = audioCtx.createGain();
        gain1.gain.value = this.gainLeft;
        oscillator1.connect(gain1);
        merger = audioCtx.createChannelMerger(2);
        silence = audioCtx.createBufferSource();
        silence.connect(merger, 0, 0);
        gain1.connect(merger, 0, 0);
        oscillator2 = audioCtx.createOscillator();
        oscillator2.frequency.value = this.right;
        gain2 = audioCtx.createGain();
        gain2.gain.value = this.gainRight;
        oscillator2.connect(gain2);
        gain2.connect(merger, 0, 1);
        merger.connect(audioCtx.destination);
        oscillator1.start(0);
        oscillator2.start(0);
        this.oscillator1 = oscillator1;
        this.oscillator2 = oscillator2;
        if (this.duration != null) {
          stopTime = audioCtx.currentTime + this.duration;
          console.log(stopTime);
          this.oscillator1.stop(stopTime);
          this.oscillator2.stop(stopTime);
          window.binauralBeatSingleton = void 0;
        }
        this.gainNode1 = gain1;
        this.gainNode2 = gain2;
      }

      BinauralBeat.prototype.change = function(left, right, gainLeft, gainRight, duration) {
        var stopTime;
        console.log("Tone changing ...");
        this.left = left;
        this.right = right;
        this.gainLeft = gainLeft;
        this.gainRight = gainRight;
        this.oscillator1.frequency.value = left;
        this.oscillator2.frequency.value = right;
        this.gainNode1.gain.value = gainLeft;
        this.gainNode2.gain.value = gainRight;
        this.duration = duration;
        if (duration != null) {
          stopTime = this.audioCtx.currentTime + this.duration;
          console.log(stopTime);
          this.oscillator1.stop(stopTime);
          this.oscillator2.stop(stopTime);
          return window.binauralBeatSingleton = void 0;
        }
      };

      BinauralBeat.prototype.stop = function() {
        this.oscillator1.stop();
        return this.oscillator2.stop();
      };

      return BinauralBeat;

    })();
    console.log("Loading Binaural Module");
    if (!window.binauralAudioCtx) {
      window.binauralAudioCtx = new AudioContext();
    }
    window.binauralBeatSingleton = void 0;
    binauralComm = function(comm, msg) {
      console.log('Starting Comm für binaural beats via web audio', comm, msg);
      comm.on_msg(function(m) {
        var data;
        data = m.content.data;
        window.message = m;
        switch (data.command) {
          case "set":
            return binauralSet(data);
          case "stop":
            return binauralStop(data);
        }
      });
      return comm.on_close(function(m) {
        return console.log('close', m);
      });
    };
    binauralSet = function(data) {
      if (window.binauralBeatSingleton != null) {
        return binauralBeatSingleton.change(data.left, data.right, data.gain_left, data.gain_right, data.duration);
      } else {
        return window.binauralBeatSingleton = new BinauralBeat(data.left, data.right, data.gain_left, data.gain_right, data.duration);
      }
    };
    binauralStop = function(data) {
      if (typeof binauralBeatSingleton !== "undefined" && binauralBeatSingleton !== null) {
        binauralBeatSingleton.stop();
      }
      return window.binauralBeatSingleton = void 0;
    };
    return {
      'binauralComm': binauralComm
    };
  });

}).call(this);

//# sourceMappingURL=binaural.js.map
