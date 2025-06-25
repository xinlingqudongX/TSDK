function sign(W) {
                                    function L(Se, ve) {
                                        return Se << ve | Se >>> 32 - ve
                                    }
                                    function I(Se, ve) {
                                        var be, le, ie, fe, xe;
                                        return ie = 2147483648 & Se,
                                        fe = 2147483648 & ve,
                                        xe = (1073741823 & Se) + (1073741823 & ve),
                                        (be = 1073741824 & Se) & (le = 1073741824 & ve) ? 2147483648 ^ xe ^ ie ^ fe : be | le ? 1073741824 & xe ? 3221225472 ^ xe ^ ie ^ fe : 1073741824 ^ xe ^ ie ^ fe : xe ^ ie ^ fe
                                    }
                                    function k(Se, ve, be, le, ie, fe, xe) {
                                        return Se = I(Se, I(I(function(De, Qe, it) {
                                            return De & Qe | ~De & it
                                        }(ve, be, le), ie), xe)),
                                        I(L(Se, fe), ve)
                                    }
                                    function G(Se, ve, be, le, ie, fe, xe) {
                                        return Se = I(Se, I(I(function(De, Qe, it) {
                                            return De & it | Qe & ~it
                                        }(ve, be, le), ie), xe)),
                                        I(L(Se, fe), ve)
                                    }
                                    function J(Se, ve, be, le, ie, fe, xe) {
                                        return Se = I(Se, I(I(function(De, Qe, it) {
                                            return De ^ Qe ^ it
                                        }(ve, be, le), ie), xe)),
                                        I(L(Se, fe), ve)
                                    }
                                    function N(Se, ve, be, le, ie, fe, xe) {
                                        return Se = I(Se, I(I(function(De, Qe, it) {
                                            return Qe ^ (De | ~it)
                                        }(ve, be, le), ie), xe)),
                                        I(L(Se, fe), ve)
                                    }
                                    function T(Se) {
                                        var ve, be = "", le = "";
                                        for (ve = 0; 3 >= ve; ve++)
                                            be += (le = "0" + (Se >>> 8 * ve & 255).toString(16)).substr(le.length - 2, 2);
                                        return be
                                    }
                                    var B, te, F, ee, ae, ue, se, oe, me, de;
                                    for (W = function(Se) {
                                        Se = Se.replace(/\r\n/g, `
`);
                                        for (var ve = "", be = 0; be < Se.length; be++) {
                                            var le = Se.charCodeAt(be);
                                            128 > le ? ve += String.fromCharCode(le) : le > 127 && 2048 > le ? (ve += String.fromCharCode(le >> 6 | 192),
                                            ve += String.fromCharCode(63 & le | 128)) : (ve += String.fromCharCode(le >> 12 | 224),
                                            ve += String.fromCharCode(le >> 6 & 63 | 128),
                                            ve += String.fromCharCode(63 & le | 128))
                                        }
                                        return ve
                                    }(W),
                                    de = function(Se) {
                                        for (var ve, be = Se.length, le = be + 8, ie = 16 * ((le - le % 64) / 64 + 1), fe = new Array(ie - 1), xe = 0, De = 0; be > De; )
                                            xe = De % 4 * 8,
                                            fe[ve = (De - De % 4) / 4] = fe[ve] | Se.charCodeAt(De) << xe,
                                            De++;
                                        return xe = De % 4 * 8,
                                        fe[ve = (De - De % 4) / 4] = fe[ve] | 128 << xe,
                                        fe[ie - 2] = be << 3,
                                        fe[ie - 1] = be >>> 29,
                                        fe
                                    }(W),
                                    ue = 1732584193,
                                    se = 4023233417,
                                    oe = 2562383102,
                                    me = 271733878,
                                    B = 0; B < de.length; B += 16)
                                        te = ue,
                                        F = se,
                                        ee = oe,
                                        ae = me,
                                        ue = k(ue, se, oe, me, de[B + 0], 7, 3614090360),
                                        me = k(me, ue, se, oe, de[B + 1], 12, 3905402710),
                                        oe = k(oe, me, ue, se, de[B + 2], 17, 606105819),
                                        se = k(se, oe, me, ue, de[B + 3], 22, 3250441966),
                                        ue = k(ue, se, oe, me, de[B + 4], 7, 4118548399),
                                        me = k(me, ue, se, oe, de[B + 5], 12, 1200080426),
                                        oe = k(oe, me, ue, se, de[B + 6], 17, 2821735955),
                                        se = k(se, oe, me, ue, de[B + 7], 22, 4249261313),
                                        ue = k(ue, se, oe, me, de[B + 8], 7, 1770035416),
                                        me = k(me, ue, se, oe, de[B + 9], 12, 2336552879),
                                        oe = k(oe, me, ue, se, de[B + 10], 17, 4294925233),
                                        se = k(se, oe, me, ue, de[B + 11], 22, 2304563134),
                                        ue = k(ue, se, oe, me, de[B + 12], 7, 1804603682),
                                        me = k(me, ue, se, oe, de[B + 13], 12, 4254626195),
                                        oe = k(oe, me, ue, se, de[B + 14], 17, 2792965006),
                                        ue = G(ue, se = k(se, oe, me, ue, de[B + 15], 22, 1236535329), oe, me, de[B + 1], 5, 4129170786),
                                        me = G(me, ue, se, oe, de[B + 6], 9, 3225465664),
                                        oe = G(oe, me, ue, se, de[B + 11], 14, 643717713),
                                        se = G(se, oe, me, ue, de[B + 0], 20, 3921069994),
                                        ue = G(ue, se, oe, me, de[B + 5], 5, 3593408605),
                                        me = G(me, ue, se, oe, de[B + 10], 9, 38016083),
                                        oe = G(oe, me, ue, se, de[B + 15], 14, 3634488961),
                                        se = G(se, oe, me, ue, de[B + 4], 20, 3889429448),
                                        ue = G(ue, se, oe, me, de[B + 9], 5, 568446438),
                                        me = G(me, ue, se, oe, de[B + 14], 9, 3275163606),
                                        oe = G(oe, me, ue, se, de[B + 3], 14, 4107603335),
                                        se = G(se, oe, me, ue, de[B + 8], 20, 1163531501),
                                        ue = G(ue, se, oe, me, de[B + 13], 5, 2850285829),
                                        me = G(me, ue, se, oe, de[B + 2], 9, 4243563512),
                                        oe = G(oe, me, ue, se, de[B + 7], 14, 1735328473),
                                        ue = J(ue, se = G(se, oe, me, ue, de[B + 12], 20, 2368359562), oe, me, de[B + 5], 4, 4294588738),
                                        me = J(me, ue, se, oe, de[B + 8], 11, 2272392833),
                                        oe = J(oe, me, ue, se, de[B + 11], 16, 1839030562),
                                        se = J(se, oe, me, ue, de[B + 14], 23, 4259657740),
                                        ue = J(ue, se, oe, me, de[B + 1], 4, 2763975236),
                                        me = J(me, ue, se, oe, de[B + 4], 11, 1272893353),
                                        oe = J(oe, me, ue, se, de[B + 7], 16, 4139469664),
                                        se = J(se, oe, me, ue, de[B + 10], 23, 3200236656),
                                        ue = J(ue, se, oe, me, de[B + 13], 4, 681279174),
                                        me = J(me, ue, se, oe, de[B + 0], 11, 3936430074),
                                        oe = J(oe, me, ue, se, de[B + 3], 16, 3572445317),
                                        se = J(se, oe, me, ue, de[B + 6], 23, 76029189),
                                        ue = J(ue, se, oe, me, de[B + 9], 4, 3654602809),
                                        me = J(me, ue, se, oe, de[B + 12], 11, 3873151461),
                                        oe = J(oe, me, ue, se, de[B + 15], 16, 530742520),
                                        ue = N(ue, se = J(se, oe, me, ue, de[B + 2], 23, 3299628645), oe, me, de[B + 0], 6, 4096336452),
                                        me = N(me, ue, se, oe, de[B + 7], 10, 1126891415),
                                        oe = N(oe, me, ue, se, de[B + 14], 15, 2878612391),
                                        se = N(se, oe, me, ue, de[B + 5], 21, 4237533241),
                                        ue = N(ue, se, oe, me, de[B + 12], 6, 1700485571),
                                        me = N(me, ue, se, oe, de[B + 3], 10, 2399980690),
                                        oe = N(oe, me, ue, se, de[B + 10], 15, 4293915773),
                                        se = N(se, oe, me, ue, de[B + 1], 21, 2240044497),
                                        ue = N(ue, se, oe, me, de[B + 8], 6, 1873313359),
                                        me = N(me, ue, se, oe, de[B + 15], 10, 4264355552),
                                        oe = N(oe, me, ue, se, de[B + 6], 15, 2734768916),
                                        se = N(se, oe, me, ue, de[B + 13], 21, 1309151649),
                                        ue = N(ue, se, oe, me, de[B + 4], 6, 4149444226),
                                        me = N(me, ue, se, oe, de[B + 11], 10, 3174756917),
                                        oe = N(oe, me, ue, se, de[B + 2], 15, 718787259),
                                        se = N(se, oe, me, ue, de[B + 9], 21, 3951481745),
                                        ue = I(ue, te),
                                        se = I(se, F),
                                        oe = I(oe, ee),
                                        me = I(me, ae);
                                    return (T(ue) + T(se) + T(oe) + T(me)).toLowerCase()
                                }